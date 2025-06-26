FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip -r requirements.txt

COPY ./app /app/app

EXPOSE 8000

# localhost:8000/docs
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]