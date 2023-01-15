FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src src
COPY data data
COPY prod.env .env

EXPOSE 80:80

CMD [ "python3", "src/server.py"]