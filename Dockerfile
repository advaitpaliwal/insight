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
    portaudio19-dev \
    python3-picamera2 \
    python3-libcamera \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN useradd --create-home appuser
USER appuser

# Copy the application code to the container
COPY --chown=appuser:appuser . .

# Expose the port the app runs on (if applicable)
EXPOSE 8000

# Run the application
CMD ["python", "-u", "/app/main.py"]