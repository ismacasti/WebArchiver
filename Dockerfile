FROM python:alpine3.7
LABEL version="1.0"
LABEL maintainer="Ismael Castiñeira<ismacasti@github>"

RUN ["pip3", "install", "requests"]
RUN ["pip3", "install", "warcio"]

ADD . /app
WORKDIR /app

ENTRYPOINT ["python3", "main.py"]
