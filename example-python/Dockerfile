# Use an official Python runtime as a parent image
FROM benchbot:latest

WORKDIR /app
COPY . /app

RUN git clone https://github.com/pjreddie/darknet && 
    mv darknet yolo && 
    cd yolo && 
    wget https://pjreddie.com/media/files/yolov3.weights && 
    make -j8

CMD ["python", "app.py"]
