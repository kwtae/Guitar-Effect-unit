# Use an official Python runtime as a parent image, optimized for size
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Install system dependencies (required for some python audio/gpio packages or psycopg2 if we swap from SQLite)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend directory contents into the container at /app/backend
# Notice we are copying the backend directory INTO a backend folder inside /app
# This preserves the python module structure `from backend.database import get_db`
COPY . /app/backend

# Set the python path so modules resolve correctly
ENV PYTHONPATH=/app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run FastAPI when the container launches using Uvicorn
# We use host 0.0.0.0 so it's accessible from other devices on the LAN (like the frontend mobile app)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
