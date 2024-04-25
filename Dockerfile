FROM python:3.11.5-slim-bullseye


RUN mkdir -p /var/app
WORKDIR /var/app

RUN apt update 
RUN apt install -y ffmpeg 

RUN pip install setuptools-rust

COPY requirments.txt /var/app
RUN pip install -r requirments.txt


COPY cache /var/app/cache
COPY src /var/app/src


EXPOSE 5000

CMD ["python", "src/server.py"]







