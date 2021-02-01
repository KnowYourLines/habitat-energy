FROM python:3.8.6-slim-buster

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

COPY . /src/
