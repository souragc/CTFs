FROM ubuntu:16.04
MAINTAINER fweasd
WORKDIR /
RUN apt update 
RUN apt install -y libssl-dev xinetd python2.7 libseccomp-dev
RUN apt autoremove && apt autoclean 
COPY ./home /home

