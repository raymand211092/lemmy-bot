FROM python:3-slim-buster

ENV token ""

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD python3 fed_ed.py ${token}