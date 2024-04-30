FROM python:3.11.5-slim-bullseye

RUN mkdir -p /var/app
WORKDIR /var/app

# Install ffmpeg and clean up in one layer to reduce image size
RUN apt-get update && apt-get install -y \
    ffmpeg \
    # Clean up
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /var/app/
RUN pip install -r requirements.txt

# Copy application code
COPY src /var/app/src

# Cache the whisper files in the container
ARG WHISPER_CACHE_DIR
ARG CONTAINER_WHISPER_CACHE_DIR=whisper_cache

COPY $WHISPER_CACHE_DIR /var/app/$CONTAINER_WHISPER_CACHE_DIR
ENV WHISPER_CACHE_DIR=$CONTAINER_WHISPER_CACHE_DIR

# Inform Docker that the container listens on the specified port at runtime.
EXPOSE 5000

# Command to run the application
CMD ["python", "src/server.py"]
