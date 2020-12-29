FROM python:3.9-alpine

# init
RUN mkdir /app
WORKDIR /app
COPY requirements /app/requirements

# setup
RUN apk update
RUN apk upgrade
RUN apk --no-cache add \
    postgresql-client \
    postgresql-dev \
    build-base \
    gettext \
    gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

RUN pip install --upgrade pip
RUN pip install -r requirements/production.txt

# clean
RUN apk del -r postgresql

# prep
ENV PYTHONUNBUFFERED 1
COPY . /app/
