FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /smarturl

WORKDIR /smarturl

COPY requirements.txt /smarturl/

RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /smarturl/