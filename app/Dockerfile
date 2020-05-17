FROM python:3.8.2-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev gettext && \
    pip install --upgrade pip && \
    pip install -r requirements.txt


ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]