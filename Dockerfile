FROM python:3.8.2

WORKDIR /root/src/

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt
