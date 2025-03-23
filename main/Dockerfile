FROM python:3.12-alpine

# Ensure Python output is displayed in real-time
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apk add --no-cache \
    mariadb-connector-c-dev \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    pkgconfig \
    mariadb-client

# Copy and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application files
COPY . /app
# Set env
ENV FLASK_APP=main.py
# Set command to run the application
CMD ["python", "main.py"]