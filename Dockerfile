FROM python:3.9-slim
WORKDIR /app
COPY wsgi.py /app/
COPY app /app/app/
RUN pip install -r /app/app/requirements.txt
CMD ["python", "wsgi.py"]
