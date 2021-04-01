# Build stage 0
FROM erlang:alpine

RUN mkdir /pkgs
WORKDIR /pkgs
RUN mkdir curl
RUN apk fetch --output curl --recursive --no-cache -- curl
RUN mkdir git
RUN apk fetch --output git --recursive --no-cache -- git
RUN mkdir make
RUN apk fetch --output make --recursive --no-cache -- make
RUN mkdir ncurses-libs
RUN apk fetch --output ncurses-libs --recursive --no-cache -- ncurses-libs

RUN apk add --no-network /pkgs/make/* /pkgs/git/*

RUN mkdir -p /buildroot
WORKDIR /buildroot

COPY Makefile Makefile
COPY erlang.mk erlang.mk
COPY relx.config relx.config
COPY config config

RUN make deps

# Build stage 1
FROM erlang:alpine

COPY --from=0 /pkgs /pkgs

RUN apk add --no-network /pkgs/curl/*
RUN apk add --no-network /pkgs/git/*
RUN apk add --no-network /pkgs/make/*

RUN mkdir -p /buildroot
WORKDIR /buildroot

COPY --from=0 /buildroot /buildroot
COPY src/add_topic_handler.erl src/
COPY src/file_handler.erl src/
COPY src/deaddrop_app.erl src/
COPY src/deaddrop_sup.erl src/
COPY src/publish_handler.erl src/
COPY src/subscribe_handler.erl src/
COPY src/subscriber_pool.erl src/
COPY src/topics_handler.erl src/

RUN make rel

# Build stage 2
FROM alpine

COPY --from=0 /pkgs /pkgs

RUN apk add --no-network /pkgs/ncurses-libs/*

# Install the released application
COPY --from=1 /buildroot/_rel /srv

# Expose relevant ports
EXPOSE 8080

CMD ["/srv/deaddrop_release/bin/deaddrop_release", "console"]
