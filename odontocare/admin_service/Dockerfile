FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY odontocare/admin_service .

EXPOSE 5000

CMD ["python", "run.py"]