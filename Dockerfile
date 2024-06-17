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