FROM python:3.11-slim

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
