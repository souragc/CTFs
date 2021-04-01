<?php


namespace App\Library;


class AppStorage
{
    const templatesDir = 'templates';
    const ticketsDir = 'tickets';
    /**
     * @var string
     */
    private $ticketBase;
    /**
     * @var string
     */
    private $templatesBase;

    private function join($d1, $d2)
    {
        if (substr_compare($d1, "/", -1) === 0) {
            $d1 = substr($d1, 0, strlen($d1) - 1);
        }
        if (substr_compare($d2, "/", 0, 1) === 0) {
            $d2 = substr($d2, 1);
        }
        return "{$d1}/{$d2}";
    }

    public function __construct($baseFolder)
    {
        $this->ticketBase = $this->join($baseFolder, self::ticketsDir);
        $this->templatesBase = $this->join($baseFolder, self::templatesDir);
    }

    public function templatePath($id)
    {
        return $this->join($this->templatesBase, strval($id) . '.html');
    }

    public function ticketPath($id)
    {
        return $this->join($this->ticketBase, $id . '.pdf');
    }

    public function ticketRenderFinishedPath($id) {
        return $this->join($this->ticketBase, $id . '.ready');
    }

    public function ticketExists($id) {
        return file_exists($this->ticketRenderFinishedPath($id)) && file_exists($this->ticketPath($id));
    }
}
