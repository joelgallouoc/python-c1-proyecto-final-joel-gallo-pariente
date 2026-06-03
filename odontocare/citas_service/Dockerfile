FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY odontocare/citas_service .

EXPOSE 5001

CMD ["python", "run.py"]