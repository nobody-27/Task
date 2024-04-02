FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /django
# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade pip