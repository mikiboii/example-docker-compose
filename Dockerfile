FROM python:3.12-slim-bookworm

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app3.py \
    FLASK_RUN_HOST=0.0.0.0

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        g++ \
        gcc \
        python3-dev \
        ffmpeg \
        libavcodec-dev \
        libavformat-dev \
        libavutil-dev \
        libswscale-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies (including pybind11)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt pybind11

# Copy ALL source files (including C++ files)
COPY . .

# Compile the C++ module
RUN python3 -c "\
import subprocess, shlex; \
py_includes = subprocess.getoutput('python3 -m pybind11 --includes'); \
extension_suffix = subprocess.getoutput('python3-config --extension-suffix'); \
cmd = [ \
    'g++', '-O3', '-Wall', '-shared', '-std=c++11', '-fPIC', \
    *shlex.split(py_includes), \
    'class_demo.cpp', \
    '-o', f'mymodule{extension_suffix}', \
    '-lavformat', '-lavcodec', '-lavutil' \
]; \
subprocess.run(cmd, check=True)"

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
