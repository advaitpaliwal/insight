# Use the official Python image for Raspberry Pi
FROM python:3.10-bullseye

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    libatlas-base-dev \
    libportaudio2 \
    libpulse-dev \
    libasound2-dev \
    libgrpc-dev \
    libcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the pyproject.toml and setup.py files to the working directory
COPY pyproject.toml setup.py ./

# Install build dependencies
RUN pip install --no-cache-dir setuptools wheel Cython

# Build and install the project dependencies
RUN pip install --no-cache-dir .

# Copy the application code to the container
COPY --chown=appuser:appuser . .

# Expose the port the app runs on (if applicable)
EXPOSE 8000

# Run the application
CMD ["python", "-u", "/app/main.py"]