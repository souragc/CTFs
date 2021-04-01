#Base Dockerfile Stage
FROM python:3.6.8-stretch as base
RUN apt-get update && apt-get install -y yasm espeak-ng ffmpeg curl

FROM base as build-dev
WORKDIR /explotify_service

RUN mkdir explotify_db
RUN mkdir music
COPY ./requirements.txt /explotify_service
RUN pip install -r requirements.txt
COPY . /explotify_service
RUN mkdir distopianM
RUN curl -L -o distopianM/distopian.mp3 https://appchama.com/distopian.mp3
RUN flask db init && flask db migrate && flask db upgrade
ENV FLASK_ENV development
ENV FLASK_APP main.py
CMD ["flask","run","-h","0.0.0.0","-p","80"]


FROM tiangolo/uwsgi-nginx-flask:python3.6 as build-prod
RUN apt-get update && apt-get install -y yasm espeak-ng ffmpeg
ENV LISTEN_PORT="80"
ENV UWSGI_PROCESSES 20
ENV UWSGI_CHEAPER 19
WORKDIR /app
RUN mkdir explotify_db
RUN mkdir music
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
RUN mkdir distopianM
RUN curl -L -o distopianM/distopian.mp3 https://appchama.com/distopian.mp3
RUN flask db init && flask db migrate && flask db upgrade
