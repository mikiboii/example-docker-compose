FROM python:3.12-slim-bookworm

WORKDIR /app

# Set environment variables (single line format)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app2.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
