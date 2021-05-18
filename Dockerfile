FROM python:3.8-slim

WORKDIR /app

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ADD . .

EXPOSE 8000