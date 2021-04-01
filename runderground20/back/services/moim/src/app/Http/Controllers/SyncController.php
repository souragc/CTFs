<?php


namespace App\Http\Controllers;


use App\Jobs\RendererJob;
use App\Library\AppStorage;
use App\Library\Renderer;
use App\Services\ChallengesService;
use App\Services\SyncService;
use App\Services\UserService;
use Illuminate\Http\Request;
use App\Library\HtmlBuilder;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\File;

class SyncController extends Controller
{

    /**
     * @var SyncService $syncService
     */
    private $syncService;
    /**
     * @var UserService
     */
    private $userService;
    /**
     * @var ChallengesService
     */
    private $challengesService;

    public function __construct(SyncService $service, UserService $us, ChallengesService $challengesService)
    {
        $this->syncService = $service;
        $this->userService = $us;
        $this->challengesService = $challengesService;
    }

    public function addSync(Request $request)
    {
        $this->validate($request, [
            'capacity' => 'required|int|between:3,50',
            'title' => 'required|string|max:100',
            'description' => 'required|string|max:500',
            'image_url' => 'url',
            'image_params' => 'array',
            'image_base64' => 'string|max:204800|regex:/^data:image\/jpeg;base64,[A-Za-z0-9=+\/]+$/m',
        ]);

        $user = Auth::user();

        $title = $request->get('title');
        $desc = $request->get('description');
        $syncData = $this->syncService->addSync($user->id,
            $title,
            $desc,
            $request->get('capacity')
        );

        if (!$syncData) {
            return \response()->json(['error' => 'Failed to add sync. Try again.'])->setStatusCode(412);
        }

        $img = null;
        if ($request->get('image_url')) {
            $img = (new HtmlBuilder())
                ->image($request->get('image_url'), 'anime', $request->get('image_params'));
        }

        /** @var UploadedFile $uploadedImg */
        $uploadedImg = $request->get('image_base64');
        if ($uploadedImg) {
            $img = (new HtmlBuilder())
                ->image($request->get('image_base64'), 'anime', $request->get('image_params'));
        }

        $data = view('base_ticket', [
            'title' => $title,
            'description' => $desc,
            'img' => $img,
        ])->render();

        /** @var AppStorage $storage */
        $storage = app(AppStorage::class);

        file_put_contents($storage->templatePath($syncData['id']), $data);
        return response()->json(['id' => $syncData['id']]);
    }

    public function getInfo($id)
    {
        $sync = $this->syncService->getSyncById($id);
        if (!$sync) {
            return response()->json(['error' => "Sync not found"])->setStatusCode(404);
        }
        $author = $this->userService->get($sync->author_id);
        return response()->json(
            ['id' => $sync->id,
                'capacity' => $sync->capacity,
                'title' => $sync->title,
                'description' => $sync->description,
                'author' => [
                    'id' => $author->id,
                    'email' => $author->email,
                ],
                'created_at' => $sync->created_at,
            ]
        );
    }

    public function list(Request $request)
    {
        $user = Auth::user();
        return response()->json($this->syncService->getUserSyncs($user->id));
    }

    public function get($id)
    {
        $user = Auth::user();
        $sync = $this->syncService->getSyncById($id);
        if (!$sync) {
            return response()->json(['error' => "Sync not found"])->setStatusCode(404);
        }
        if ($sync->author_id != $user->id) {
            return response()->json(['error' => "Unauthorized"])->setStatusCode(403);
        }
        return response()->json($this->syncService->listMembers($sync->id));
    }

    public function challenge()
    {
        $user = Auth::user();
        $challenge = $this->challengesService->generate($user->id);
        if (!$challenge) {
            return response()->json(['error' => "Failed to generate challenge"])->setStatusCode(412);
        }
        return response()->json(['challenge' => $challenge]);
    }

    public function addMember($id)
    {
        $user_id = Auth::user()->id;
        // You can't change the challenge as it is used by checker and frontend.
        $answer = \request('challenge_answer');
        if (!$this->challengesService->validate($user_id, $answer)) {
            return response()->json(['error' => "Invalid challenge answer"])->setStatusCode(429);
        }

        $sync = $this->syncService->getSyncById($id);
        if (!$sync) {
            return response()->json(['error' => "Sync not found"])->setStatusCode(404);
        }

        $this->validate(\request(), [
            'nickname' => 'required|string|between:3,50',
        ]);

        $nickname = \request('nickname');
        $data = $this->syncService->addMember($sync, $nickname);
        if (!$data) {
            return \response()->json(['error' => 'Failed to add member. Try again later.'])->setStatusCode(503);
        }

        /** @var AppStorage $storage */
        $storage = app(AppStorage::class);

        $template = $storage->templatePath($sync->id);
        if (!file_exists($template)) {
            return \response()->json(['error' => 'Failed to find sync template.'])->setStatusCode(503);
        }

        $public_id = $data['public_id'];
        dispatch(new RendererJob($template, $nickname, $public_id));
        return \response()->json(['public_id' => $public_id, 'message' => 'You ticket will be rendered soon']);
    }

    public function ticket($id)
    {
        $info = $this->syncService->getTicketInfo($id);
        if (!$info) {
            return response()->json(['error' => "Sync not found"])->setStatusCode(404);
        }
        $publicId = $info->public_id;
        $syncId = $info->sync_id;
        $sync = $this->syncService->getSyncById($syncId);
        $syncData = [
            'title' => $sync->title,
            'description' => $sync->description,
        ];

        $jsonData = [
            'sync' => $syncData, 'nickname' => $info->nickname, 'public_id' => $publicId,
        ];

        /** @var AppStorage $storage */
        $storage = app(AppStorage::class);
        if ($storage->ticketExists($publicId)) {
            $jsonData['ticket_url'] = '/tickets/' . $publicId . '.pdf';
        }

        return response()->json($jsonData);
    }

    public function latestSyncs()
    {
        return response()->json($this->syncService->latestSyncs());
    }
}
