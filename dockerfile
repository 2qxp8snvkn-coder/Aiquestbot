# Use an official lightweight Python image.
FROM python:3.9-slim

# Set environment variables in the container.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory.
WORKDIR /app

# Install dependencies specified in requirements.txt.
COPY requirements.txt .
RUN pip install --upgrade pip -r requirements.txt --no-cache-dir

# Copy project files into the container’s filesystem at /app/.
COPY . .

CMD ["python", "main.py"]
