# Dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.settings

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy project requirements
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Create directory for file uploads
RUN mkdir -p /app/media/uploads

# Expose ports
EXPOSE 8000

# Run Django migrations and start server with FastAPI
CMD ["sh", "-c", "python manage.py migrate && uvicorn fast_api_app.main:app --host 0.0.0.0 --port 8000"]


# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=data_platform
    ports:
      - "5432:5432"

  web:
    build: .
    command: sh -c "python manage.py migrate && uvicorn fast_api_app.main:app --host 0.0.0.0 --port 8000"
    volumes:
      - .:/app
      - ./media:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/data_platform
      - DJANGO_SETTINGS_MODULE=core.settings
      - DEBUG=True

volumes:
  postgres_data: