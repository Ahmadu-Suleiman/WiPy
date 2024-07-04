# Use an Alpine-based Python image (ensure this is a stable version)
FROM python:3.9-alpine

# Upgrade apk and install necessary packages
RUN apk update && \
    apk add --no-cache build-base libffi-dev openssl-dev

# Install pip if it's not already installed
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app


# Copy your application code into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Start your application
CMD ["python", "app.py"]
