FROM python:3.9-slim
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY ./e_commerce/ /app/
# COPY wait-for-postgres.sh /app/
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

