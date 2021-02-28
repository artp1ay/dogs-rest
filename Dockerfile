FROM python:3.8.1

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .