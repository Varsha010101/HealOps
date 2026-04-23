FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--workers", "2", "--threads", "2", "--timeout", "0", "-b", "0.0.0.0:5000", "app:app"]