-module(topics_handler).
-behavior(cowboy_handler).

-export([init/2]).

init(Req0=#{method := <<"GET">>}, State) ->
    Topics = gen_event:call({global, file_handler}, file_handler, {topics}),
    Req = case catch hd(Topics) of
        {'EXIT', {badarg, _}} ->
            cowboy_req:reply(200, #{<<"content-type">> => <<"text/plain">>}, [""], Req0);
        _ ->
            CleanedTopics = lists:map(fun remove_private_topics/1, Topics),
            cowboy_req:reply(200, #{<<"content-type">> => <<"text/plain">>}, [CleanedTopics], Req0)
    end,

    {ok, Req, State};

init(Req0, State) ->
    Req = cowboy_req:reply(405, #{
        <<"allow">> => <<"GET">>
    }, Req0),
    {ok, Req, State}.

remove_private_topics(String) ->
    case string:prefix(String, "- ") of
        nomatch -> String ++ "\n";
        _ -> "\n"
    end.
