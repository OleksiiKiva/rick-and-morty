FROM python:3.12.3-alpine3.19
LABEL maintainer="oleksii.kiva@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
