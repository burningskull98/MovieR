FROM python:3.13

WORKDIR /app/PythonProject

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .


RUN pip3 install --upgrade pip && pip3 install -r requirements.txt


RUN pip3 install gunicorn


COPY . .


EXPOSE 8080