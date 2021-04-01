-module(publish_handler).
-behavior(cowboy_handler).

-export([init/2]).

init(Req0=#{method := <<"POST">>}, State) ->
    Req = case cowboy_req:read_body(Req0) of
        {ok, Data, _} when erlang:size(Data) =< 7000 ->
            Message = string:tokens(string:trim(binary_to_list(Data)), ":"),
            Topic = hd(Message),
            Content = hd(tl(Message)),
            % Trigger saving
            gen_event:notify({global, file_handler}, {new, {Topic, Content}}),
            % Trigger publish
            Reply = gen_server:call({global, subscriber_pool}, {"New MSG", Topic, Content}),
            cowboy_req:reply(200, #{<<"content-type">> => <<"text/plain">>}, list_to_binary(Reply), Req0);
        {ok, _, _} ->
            cowboy_req:reply(400, #{<<"content-type">> => <<"text/plain">>}, ["Bad Request."], Req0);
        {_} ->
            io:fwrite("Got an error while parsing request body."),
            "Parsing Error."
    end,
    {ok, Req, State};

init(Req0, State) ->
    Req = cowboy_req:reply(405, #{
        <<"allow">> => <<"POST">>
    }, Req0),
    {ok, Req, State}.
