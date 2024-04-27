FROM python:3.10-slim

WORKDIR /home

COPY ./requirements.txt ./

RUN apt-get update -y

RUN apt-get install curl -y

RUN pip install -r requirements.txt

CMD uvicorn main:app --reload --port 8001

EXPOSE 8001
