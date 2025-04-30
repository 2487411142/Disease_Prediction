FROM python:3.10

WORKDIR /app
RUN ["pip", "install", "--no-cache-dir", "--upgrade", "pip"]
COPY backend/requirements.txt .
RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

COPY backend backend
COPY disease_files disease_files
CMD ["python", "backend/app.py"]