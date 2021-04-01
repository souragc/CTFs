FROM python:3.6.8-stretch as base


FROM base as build-dev
WORKDIR /db_engine_explotify
COPY . /db_engine_explotify
RUN pip install -r requirements.txt
CMD ["python","main.py"]

FROM tiangolo/uwsgi-nginx-flask:python3.6 as build-prod
WORKDIR /app
COPY . /app
ENV LISTEN_PORT="80"
RUN pip install -r requirements.txt

