# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

ADD . /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Install the dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Define environment variable
ENV NAME World

# Command to run the app using Gunicorn
CMD ["gunicorn", "-b", ":8080", "wsgi:app"]