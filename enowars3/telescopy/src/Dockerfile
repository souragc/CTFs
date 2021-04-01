FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY . /app
WORKDIR /app

RUN chmod +x ticketChecker

RUN pip install -r requirements.txt
