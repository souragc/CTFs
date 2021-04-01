FROM ubuntu:18.04

RUN  dpkg --add-architecture i386 && \
     apt-get -y update  && \
     apt-get -y install xinetd && \
     apt-get -y install libc6:i386 libncurses5:i386 libstdc++6:i386


RUN useradd -m ctf

ADD start.sh /root
ADD chall /home/ctf
ADD flag /home/ctf
ADD run.sh /home/ctf
ADD chall.xinetd /etc/xinetd.d/chall

RUN chmod +x /root/start.sh && \
    chmod +x /home/ctf/chall && \
    chmod +x /home/ctf/run.sh && \
    chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf/   && \
    chown root:ctf /home/ctf/flag && \
    chmod 440 /home/ctf/flag  && \
    chmod 755 /tmp 

ENTRYPOINT  /root/start.sh
