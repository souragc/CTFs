-module(deaddrop_sup).
-behaviour(supervisor).

-export([start_link/0]).
-export([init/1]).

start_link() ->
	supervisor:start_link({local, ?MODULE}, ?MODULE, []).

init([]) ->
	SubPool = #{id => subscriber_pool, start => {gen_server, start_link, [{global, subscriber_pool}, subscriber_pool, [], []]}},
	% Using this would be prefered but we don't know where to register a callback with this process within app startup.
	% FileHandler = #{id => file_handler, start => {gen_event, start_link, [{global, file_handler}]}},
	{ok, Pid} = gen_event:start_link({global, file_handler}),

	gen_event:add_sup_handler(Pid, file_handler, []),

	% {ok, {{one_for_one, 1, 5}, [SubPool, FileHandler]}}.
	{ok, {{one_for_one, 1, 5}, [SubPool]}}.

