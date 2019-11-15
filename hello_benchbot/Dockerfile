# Create a base image which provides all of your dependencies (Ubuntu, &
# benchbot_api here)
# TODO clean this up / make a BenchBot Docker image instead of building on a
# base Ubuntu image (all of the grossness in the below paragraph should go away
# and be replaced by simply "FROM benchbot:base")
FROM ubuntu:bionic
ENV TZ "Etc/UTC"
RUN echo "$TZ" > /etc/timezone && \                                             
    ln -s /usr/share/zoneinfo/"$TZ" /etc/localtime && apt update && \
    apt install -y libsm6 libxext6 libxrender-dev python python-pip python-tk
RUN pip install benchbot_api matplotlib

# Add the files from your solution
WORKDIR /benchbot_submission
ADD hello_benchbot .
ADD line_agent.py .

# Make the command used to run your solution the default command
CMD python hello_benchbot
