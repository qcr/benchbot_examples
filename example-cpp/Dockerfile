# Use an official Python runtime as a parent image
FROM benchbot:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Compile project using either g++ or cmake
RUN g++ main.cpp `pkg-config --cflags --libs benchbot` -lbenchbot -o main

# Run the project when the container launches
CMD ["./main"]
