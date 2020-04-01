# Use a base image which provides as many of your dependencies as possible
FROM benchbot/submission:base

# Install any extra dependencies you may have
RUN pip3 install numpy

# Add the files from your solution
ADD ./hello_active .
ADD ./interactive_agent.py .

# Make the command used to run your solution the default command
CMD ./hello_active
