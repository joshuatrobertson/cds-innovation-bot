# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Install the dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Set the environment variables
ENV FLASK_APP=wsgi:app

# Command to run the app using Gunicorn
CMD ["gunicorn", "-b", ":8080", "wsgi:app"]