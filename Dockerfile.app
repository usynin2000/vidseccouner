FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Устанавливаем Flask напрямую
RUN pip install flask
RUN pip install web3
RUN pip install python-dotenv

COPY server.py /app/
COPY config.py /app/
COPY compiled.json /app/
COPY .env /app/

CMD ["python", "-u", "server.py"]
