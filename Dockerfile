FROM debian:bullseye

RUN apt update && apt install -y --no-install-recommends gnupg

RUN echo "deb http://archive.raspberrypi.org/debian/ bullseye main" > /etc/apt/sources.list.d/raspi.list \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E

RUN apt update && apt -y upgrade

RUN apt update && apt install -y --no-install-recommends \
    python3-pip \
    python3-picamera2 \
    libatlas-base-dev \
    libportaudio2 \
    libpulse-dev \
    libasound2-dev \
    libgrpc-dev \
    libcap-dev \
    portaudio19-dev \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN useradd --create-home appuser
USER appuser

# Copy the application code to the container
COPY --chown=appuser:appuser . .

# Expose the port the app runs on (if applicable)
EXPOSE 8000

# Run the application
CMD ["python", "-u", "/app/main.py"]