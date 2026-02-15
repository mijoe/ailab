# Use a lightweight Python image
FROM mcr.microsoft.com/devcontainers/python:3.11

# Optional: Install system dependencies for vector databases or data science
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt-get/lists/*

# Upgrade pip
RUN pip install --upgrade pip
