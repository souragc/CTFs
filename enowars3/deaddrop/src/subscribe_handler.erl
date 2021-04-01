-module(subscribe_handler).
-behaviour(cowboy_handler).

-export([init/2, websocket_init/1, websocket_handle/2, websocket_info/2]).

init(Req0, State) ->
    % gen_server:cast({global, subscriber_pool}, {"New WS", self()}),
    {cowboy_websocket, Req0, State, #{idle_timeout => 120000}}.

websocket_init(State) ->
    io:fwrite("WS State: ~p \n", [State]),
    {reply, {text, "Heyhey from WS Handler.."}, State}.


websocket_handle({text, MessageBin}, State) ->
    List = string:tokens(binary_to_list(MessageBin), ":"),
    Reply = case length(tl(List)) of
        N when N == 1 ->
            Method = hd(List),
            Content = hd(tl(List)),
            % Remove whitespaces and newlines
            Topic = string:trim(Content),
            create_reply(Method, Topic);
        _ ->
            "Bad Request."
    end,
    {reply, {text, list_to_binary(Reply)}, State};

websocket_handle(_Frame, State) ->
    {ok, State}.

create_reply(Method, Topic) ->
    case check_topic(Topic) of
        true ->
            StrippedTopic = strip_prefix(Topic),
            case Method of
                "SUBSCRIBE" ->
                    subscribe(StrippedTopic),
                    "Subscribed.";
                "REPLAY" ->
                    Result = replay(StrippedTopic),
                    Result ++ "\n\n Finished replay.";
                _ -> "Invalid Method."
            end;
        false -> "Unknown Topic."
    end.

strip_prefix(Topic) ->
    case string:prefix(Topic, "- ") of
        nomatch ->
            case string:prefix(Topic, "+ ") of
                nomatch -> Topic;
                PublicTopic -> PublicTopic
            end;
        PrivateTopic -> PrivateTopic
    end.


subscribe(Topic) ->
    gen_server:cast({global, subscriber_pool}, {"New SUB", self(), Topic}).

replay(Topic) ->
    Result = gen_event:call({global, file_handler}, file_handler, {replay, Topic}),
    Result.

check_topic(Topic) ->
    Topics = gen_event:call({global, file_handler}, file_handler, {topics}),
    lists:member(Topic, Topics).

websocket_info({publish, Text}, State) ->
    {reply, {text, Text}, State};

websocket_info(_Info, State) ->
    {ok, State}.

