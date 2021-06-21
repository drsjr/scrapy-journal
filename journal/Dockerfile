# Use an official Python runtime as an image
FROM python:3.6

# The EXPOSE instruction indicates the ports on which a container # # will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 6800

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this
# instruction creates a directory with this name if it doesn’t exist
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY ./requirements.txt ./
COPY ./initialize.sh ./

RUN apt-get -y update
RUN apt-get -y install git
RUN pip3 install --no-cache-dir -r requirements.txt
# Run app.py when the container launches
COPY /journal/. .
CMD [ "bash", "./initialize.sh" ]