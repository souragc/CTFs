-module(deaddrop_app).
-behaviour(application).

-export([start/2]).
-export([stop/1]).


start(_Type, _Args) ->
    Dispatch = cowboy_router:compile([
            {'_', [{"/publish", publish_handler, []},
            {"/subscribe", subscribe_handler, []},
            {"/topics", topics_handler, []},
            {"/add_topic", add_topic_handler, []}
        ]}
    ]),
    % TODO: Lower the amount of allowed connections?
    {ok, _} = cowboy:start_clear(api_listener,
        [{port, 8080}, inet6],
        #{env => #{dispatch => Dispatch}}
    ),
    cowboy:set_env(api_listener, dispatch, Dispatch),
	deaddrop_sup:start_link().

stop(_State) ->
	ok.
