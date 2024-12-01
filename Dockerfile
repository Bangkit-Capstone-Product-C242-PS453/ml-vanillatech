# Gunakan image dasar Python
FROM python:3.10-slim

# Install Git dan Git LFS
RUN apt-get update && apt-get install -y git-lfs

# Inisialisasi Git LFS
RUN git lfs install

# Set environment variables to optimize Python behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required by TensorFlow and image processing
RUN apt-get install -y --no-install-recommends \
    libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Salin seluruh kode aplikasi ke dalam container
COPY . /app

# Unduh file LFS jika perlu
RUN git lfs pull

# Expose port 8080
EXPOSE 8080

# Default command to run the application
CMD ["python", "main.py"]
