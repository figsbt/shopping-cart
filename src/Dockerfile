FROM python:3.11.1-slim

WORKDIR /src


COPY . .
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN \
 pip install --upgrade pip && \
 python3 -m pip install -r requirements.txt --no-cache-dir

RUN apt install -y postgresql-client
