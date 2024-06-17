FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy application files
COPY wsgi.py /app/
COPY app /app/app/

# Run the application
CMD ["python", "wsgi.py"]
