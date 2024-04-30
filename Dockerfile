FROM python:3.11.5-slim-bullseye

RUN mkdir -p /var/app
WORKDIR /var/app

# Install ffmpeg and clean up in one layer to reduce image size
RUN apt-get update && apt-get install -y \
    ffmpeg \
    # Clean up
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /var/app/

# Install openai-whisper and cache the models
RUN version=$(grep "openai-whisper==" requirements.txt | cut -d'=' -f3) && \
    pip install openai-whisper==$version

COPY cache_whisper_models.py /var/app/
RUN python cache_whisper_models.py

# Install Python dependencies
COPY requirements.txt /var/app/
RUN pip install -r requirements.txt

# Copy application code
COPY src /var/app/src

# Cache the whisper files in the container
ARG WHISPER_CACHE_DIR
COPY $WHISPER_CACHE_DIR /var/app/$WHISPER_CACHE_DIR
ENV WHISPER_CACHE_DIR=$WHISPER_CACHE_DIR

# Inform Docker that the container listens on the specified port at runtime.
EXPOSE 5000

# Command to run the application
CMD ["python", "src/server.py"]
