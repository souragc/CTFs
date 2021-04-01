%%% counter_server.erl
-module(subscriber_pool).
-behavior(gen_server).

% API
-export([new/0]).

% required by gen_server
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3]).

%%% API methods
new() ->
  gen_server:start(?MODULE, [], []).


%%% gen_server callbacks
%%%   these are required to implement the gen_server behavior
%%%   we're really only using init and handle_call
init([]) ->
  % the second value is the initial state, an empty dict.
  {ok, [dict:new()]}.

handle_call(Request, _From, State) ->
  {_Method, Topic, Message} = Request,
  % State is a list of one dict.
  ResponseMsg = case dict:find(Topic, hd(State)) of
    {ok, Value} ->
      case notify_subscribers(Value, Message) of
        done -> "Processed PUBLISH.";
        error -> "Error returned by notify_subscribers."
      end;
    error -> "No subscriber for given Topic."
  end,
  {reply, ResponseMsg, State}.

handle_cast(Request, State) ->
  {Method, From, Topic} = Request,
  NewState = case Method of
    "New SUB" -> [dict:append(Topic, From, hd(State))];
    _ ->
      io:fwrite("Invalid Method."),
      State
  end,
  {noreply, NewState}.

% Iteratre over list of PIDs and send msg to each.
notify_subscribers([], _) ->
  done;
notify_subscribers([Head | Tail], Message) ->
  Head ! {publish, Message},
  notify_subscribers(Tail, Message).


% basically, we ignore these, but keep the same counter state
handle_info(_Msg, N) -> {noreply, N}.
code_change(_OldVsn, N, _Other) -> {ok, N}.
terminate(_Reason, _N) -> ok.
