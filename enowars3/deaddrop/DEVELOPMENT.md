Development Notes
=================

Development
-----------

### Debugging

1.	Start the Docker with the service.
2.	Run `docker attach service_queue_1` to see log messages.
3.	Interact with the service and watch the log messages.

General Details
---------------

-	Listening port: 8080

### Endpoints

-	`/publish`
	-	POST
	-	Payload: `Topic 1:message_string`
	-	Sends call to event handler `file_handler` to save received msg to file `Topic 1_msg_save.txt`
-	`/subscribe`
	-	Upgrades to Websocket automatically
	-	When connected use `SUBSCRIBE: topicname` to subscribe to topics
	-	Use `REPLAY: topicname` to receive all messages sent to Topic `topicname`
-	`/topics`
	-	GET
-	`/add_topic`
	-	PATCH
	-	Payload:
		-	`- topicname` for private topics
		-	`+ topicname` or `topicname` for public topics
	-	Creates file `topicname_msg_save.txt`. The file is used to store messages sent to this topic

### Other Processes

-	`subscriber_pool`: A server process that saves all subscribers within its state. The state contains a single dict that has topics as keys and lists of PIDs as values. Each PID represents the WS connection to the subscriber of a topic. Casts (async) are used by the `/publish` endpoint to notify the `subscriber_pool` of incoming messages.

-	`file_handler`: Event handler used to access message save files. As there is no concept of locks within Erlang a single process is used to access the message files. Notifys (async) are used to read from the files. Calls (sync) are used to write to the files.

### Dependencies

-	Erlang 21
