FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y curl netcat iproute2 golang git tar xz-utils

RUN mkdir /service
WORKDIR /service

# RUN go build -o main src/*.go && ./main
CMD ["bash", "-c", "go build -o main *.go && ./main"]
