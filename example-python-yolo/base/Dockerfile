# Use an official Python runtime as a parent image
FROM nvidia/cuda:8.0-cudnn5-devel-ubuntu16.04

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y python-pip libopencv-dev wget
RUN pip install benchbot

RUN cd yolo && git clone https://github.com/pjreddie/darknet && patch -p0 < python-yolo.patch && cd darknet && make -j8 && wget https://pjreddie.com/media/files/yolov3.weights
