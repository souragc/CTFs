-module(file_handler).
-behaviour(gen_event).

-export([init/1, handle_event/2, handle_call/2, terminate/2]).

init(_) ->
    FileName = "topics.txt",
	PrivPath = get_priv_path(FileName),
    case filelib:ensure_dir(PrivPath) of
        ok -> null;
        {error, Reason} -> io:fwrite("could not find/create path to topics.txt: ~p \n", [Reason])
    end,
    case file:open(PrivPath, [write]) of
        {ok, _} ->
                null;
        {error, Error} -> io:fwrite("Got error while creating topics.txt: ~p \n", [Error])
    end,

    io:fwrite("Initialised file_handler"),
    {ok, self()}.

% Event: {method, msg}
handle_event(Event, State) ->
    case Event of
        {new, {Topic, Message}} -> save_message(Topic, Message);
        {replay, _} -> ok
    end,
    {ok, State}.

handle_call(Event, State) ->
    case Event of
        {replay, Topic} ->
            Messages = retrieve_messages(Topic),
            {ok, Messages, State};
        {create_save, Topic} ->
            case create_message_save(Topic) of
                {ok} -> {ok, ok, State};
                {error, Msg} -> {ok, Msg, State}
            end;
        {topics} ->
            Topics = retrieve_topics(),
            {ok, Topics, State};
        {new_topic, Topic} ->
            append_topic(Topic),
            {ok, ok, State}

    end.

terminate(_Args, Fd) ->
    file:close(Fd).

create_message_save(Topic) ->
    FileName = io_lib:format("~s.txt", [Topic]),
    Path = get_priv_path(FileName),
    case file:open(Path, [append]) of
        {ok, Fh} ->
            file:write(Fh, io_lib:format("All messages sent on topic: ~s\n", [Topic])),
            {ok};
        {error, _} -> {error, "Error while creating message save."}
    end.

save_message(Topic, Message) ->
    FileName = Topic ++ ".txt",
    Path = get_priv_path(FileName),
    case file:open(Path, [append]) of
        {ok, Fh} -> file:write(Fh, "** " ++ Message ++ "\n");
        {error, _} -> io:fwrite("Error while saving message")
    end.

retrieve_messages(Topic) ->
    FileName = Topic ++ ".txt",
    Path = get_priv_path(FileName),
    {ok, Binary} = file:read_file(Path),
    binary_to_list(Binary).

retrieve_topics() ->
    FileName = "topics.txt",
    Path = get_priv_path(FileName),
    {ok, Binary} = file:read_file(Path),
    Topics = binary_to_list(Binary) ++ "- topics",
    string:tokens(Topics, "\n").

append_topic(Topic) ->
    FileName = "topics.txt",
    % Check if the topic is indicated as private, otherwise prepend a '+'
    NewTopic = Topic ++ "\n",
    % Write new Topic to topics file
    Path = get_priv_path(FileName),
    case file:open(Path, [append]) of
        {ok, Fh} ->
            file:write(Fh, NewTopic),
            {ok};
        {error, _} -> {error, "Error while saving new topic."}
    end.

get_priv_path(FileName) ->
    Path = case code:priv_dir(deaddrop) of
        {error, bad_name} ->
            "priv";
        PrivDir ->
            PrivDir
    end,
    filename:join([Path, FileName]).
