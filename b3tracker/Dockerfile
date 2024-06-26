FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

ENV PORT 8080

WORKDIR /app

COPY . /app/

RUN apt-get update

RUN apt-get install -y redis-server

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD gunicorn server.wsgi:application --bind 0.0.0.0:"${PORT}"

EXPOSE ${PORT}
