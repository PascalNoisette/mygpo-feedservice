FROM python:3.8-alpine as base

FROM base as builder

WORKDIR /usr/src/

RUN mkdir /usr/src/mygpo

RUN apk update && apk add git postgresql-dev gcc python3-dev musl-dev libffi-dev zlib-dev jpeg-dev

COPY requirements.txt /usr/src/mygpo/requirements.txt

WORKDIR /usr/src/mygpo 

RUN pip install -r requirements.txt --prefix=/install

FROM base

COPY . /usr/src/mygpo

COPY --from=builder /install /usr/local

WORKDIR /usr/src/mygpo 

RUN apk update && apk add libpq libwebp libjpeg

EXPOSE 8000

CMD [ "gunicorn", "-b", ":8000", "feedservice.wsgi" ]
