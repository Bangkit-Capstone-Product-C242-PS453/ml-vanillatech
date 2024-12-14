# Use Python base image
FROM python:3.10-slim

# Install Git and Git LFS
# RUN apt-get update && apt-get install -y \
#     git \
#     git-lfs \
#     libglib2.0-0 \
#     libsm6 \
#     libxext6 \
#     libxrender-dev \
#  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Initialize Git LFS
# RUN git lfs install

# Set environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire application code into the container
COPY . /app

# Pull LFS files if necessary
# RUN git lfs pull

# Expose port 8080 (default for Cloud Run)
EXPOSE 8080

# Default command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
