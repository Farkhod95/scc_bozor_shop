FROM python:3.14

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Update and install required packages
RUN apt-get update && \
    apt-get -y install netcat-openbsd && \
    apt-get -y install gettext && \
    apt-get -y install nano

RUN mkdir /code

COPY . /code/
RUN pip install -r /code/requirements/dev.txt
WORKDIR /code