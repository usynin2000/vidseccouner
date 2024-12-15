FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Устанавливаем Flask напрямую
RUN pip install flask

COPY server.py /app/

CMD ["python", "-u", "server.py"]
