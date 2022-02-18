FROM python:3.10.2-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD . /cvk
WORKDIR /cvk

EXPOSE $PORT
