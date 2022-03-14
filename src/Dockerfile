FROM python:3.10.0-slim-buster AS base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY ./requirements ./requirements

FROM base as prod
RUN pip install --upgrade pip && pip install -r requirements/prod.txt --no-cache-dir
COPY . /code

FROM base as test
RUN pip install --upgrade pip && pip install -r requirements/test.txt --no-cache-dir
COPY . /code

