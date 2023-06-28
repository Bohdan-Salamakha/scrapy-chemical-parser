FROM python:3.10.7-alpine
LABEL maintainer="allen.avanheim@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app
COPY pyproject.toml /app/

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /app
