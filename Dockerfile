# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
ADD . /app

# Install the dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose the port that the app runs on
EXPOSE 8000

# Set the environment variables
ENV FLASK_APP=wsgi.py

# Command to run the app using Gunicorn
CMD ["gunicorn", "-b", ":8080", "app"]