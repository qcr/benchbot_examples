# Use an official Python runtime as a parent image
FROM nvidia/cuda:8.0-cudnn5-devel-ubuntu16.04

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y python-pip libopencv-dev
RUN pip install benchbot

#CMD ["python", "app.py"]
