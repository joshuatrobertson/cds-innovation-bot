# Use the official slim Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app/
COPY requirements.txt /app/

# Install the dependencies specified in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app

# Expose port 8000 to the outside world
EXPOSE 8080

# Define the command to run the application using gunicorn
CMD ["gunicorn", "-b", ":8000", "wsgi:app"]