# Use a lightweight Python version
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your backend code
COPY . .

# Heroku assigns a dynamic port, so we use the $PORT environment variable
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}