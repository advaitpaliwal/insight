# Stage 1: Build stage
# Use a specific version of the official Python image
FROM python:3.10 as builder

# Set the working directory
WORKDIR /app

# Install system dependencies required for OpenCV
# RUN apt-get update \
#     && apt-get install -y libgl1-mesa-glx \
#     && rm -rf /var/lib/apt/lists/*

# Install dependencies in a virtual environment to keep the runtime image clean
COPY requirements.txt .
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.10

# Create a non-root user and switch to it
RUN useradd --create-home appuser

# Install system dependencies required for OpenCV in the runtime stage
# RUN apt-get update \
#     && apt-get install -y libgl1-mesa-glx \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /home/appuser
USER appuser

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv

# Set environment variable to ensure the virtual environment is activated
ENV PATH="/venv/bin:$PATH"
ENV PORT=8000

# Copy the application code to the container
COPY --chown=appuser:appuser . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD python -u "/src/main.py"
