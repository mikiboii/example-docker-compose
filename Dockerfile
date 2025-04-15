FROM python:3.12-slim-bookworm

WORKDIR /app

# Set environment variables (single line format)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app3.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/* && \
    export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH && \
    pip install pybind11 && \
    sudo apt update && \
    sudo apt install ffmpeg libavcodec-dev libavformat-dev libavutil-dev libswscale-dev && \
    g++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) class_demo.cpp -o mymodule$(python3-config --extension-suffix) -lavformat -lavcodec -lavutil


# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
