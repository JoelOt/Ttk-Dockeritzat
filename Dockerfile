FROM python:3.10.12

RUN apt-get update && apt-get install -y python3-tk && apt install sqlite3

WORKDIR /app

COPY . .

ENV DISPLAY=:0

CMD python3 ./index.py