FROM python:3.11.5-slim-bullseye

RUN mkdir -p /var/app
WORKDIR /var/app

RUN apt-get update && apt-get install -y \
    ffmpeg 

RUN pip install setuptools-rust

COPY requirements.txt /var/app
RUN pip install -r requirements.txt

COPY cache /var/app/cache
COPY src /var/app/src

ARG CACHE_WHISPER_MODELS=true
COPY cache_whisper_models.py /var/app
RUN if [ "$CACHE_WHISPER_MODELS" = "true" ] ; then python cache_whisper_models.py ; fi

EXPOSE 5000

CMD ["python", "src/server.py"]







