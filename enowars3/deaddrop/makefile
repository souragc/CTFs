# This is a development makefile. When invoking make(1), the "makefile" is
# picked up before "Makefile". Use the -f flag to specify the other makefile if
# you need to interact with Erlang.mk, e.g.: make -f Makefile deps.

.PHONY: up
up:
	docker-compose up --build -d

.PHONY: down
down:
	docker-compose down

