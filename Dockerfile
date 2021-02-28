FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
#как я понимаю это твоя команда для запуска сервера
CMD [ "python", "main.py"]
