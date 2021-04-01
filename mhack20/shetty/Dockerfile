FROM python:3

RUN apt-get update \
    && apt-get install -y socat python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install PyCryptodome

RUN useradd -Ms /bin/false ctf

WORKDIR /opt/saas

RUN mkdir storage && chmod 0777 storage
VOLUME /opt/saas/storage

COPY saas .
COPY runner.py .
RUN chmod 0755 saas runner.py

USER ctf

ENV TERM xterm
ENV LINES 24
ENV COLUMNS 80
ENV NO_COLOR 1

ENV PYTHONUNBUFFERED 1

ENTRYPOINT socat \
    TCP-LISTEN:1337,fork,reuseaddr,bind=0.0.0.0 \
    EXEC:"./runner.py ./storage ./saas",stderr,pty,echo=0,raw
EXPOSE 1337
