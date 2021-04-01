# echo 'hxp{flag}' > flag.txt && docker build -t flag_concat . && docker run -d --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -p 7777:1024 flag_concat && nc 127.0.0.1 7777

FROM debian:stretch

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd /sbin/

COPY vuln flag.txt /home/ctf/

# sane defaults
RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd

RUN chmod 555 vuln && \
    chmod 444 flag.txt

USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock)'
USER root

EXPOSE 1024
CMD ["ynetd", "-u", "ctf", "/home/ctf/vuln"]
