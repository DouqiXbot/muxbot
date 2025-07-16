# Use official Python image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p /app/fonts /app/database

# Download the font file
RUN curl -L https://github.com/DevXkirito/Vidburner/raw/main/fonts/HelveticaRounded-Bold.ttf -o /app/fonts/HelveticaRounded-Bold.ttf

# Initialize the database
RUN python -c "from database.db import db; db.setup()"

# Set the entrypoint
CMD ["python", "bot.py"]
