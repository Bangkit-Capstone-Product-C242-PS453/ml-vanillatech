# Use a lightweight Python base image
FROM python:3.10-slim

# Set environment variables to optimize Python behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required by TensorFlow and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/requirements.txt

# Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire application code into the container
COPY . /app

# Expose port 8080
EXPOSE 8080

# Define the default command to run the application
CMD ["python", "main.py"]
