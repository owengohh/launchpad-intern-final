# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# COPY current directory into the container
COPY ./app /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Upgrade pip
RUN pip install --upgrade pip

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run tests
RUN pytest

# Expose the port the app runs on
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]