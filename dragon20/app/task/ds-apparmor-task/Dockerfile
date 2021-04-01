FROM ubuntu:18.04
RUN apt update -y
RUN apt install -y docker.io xxd wget
# fix for CVE-2019-16884 is not backported to ubuntu yet :(
RUN wget https://github.com/opencontainers/runc/releases/download/v1.0.0-rc9/runc.amd64 -O /usr/sbin/runc
COPY config.json /root/.docker/config.json
COPY flag.txt /flag.txt
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD /start.sh

