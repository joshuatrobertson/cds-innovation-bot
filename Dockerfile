FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY wsgi.py /app/
COPY app /app/app/

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy application files
COPY wsgi.py /app/
COPY app /app/app/

# Run the application
CMD ["python", "wsgi.py"]