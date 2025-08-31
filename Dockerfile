# Use official Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .
COPY runtime.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Environment variables (can be overridden by Koyeb dashboard)
ENV PYTHONUNBUFFERED=1

# Default command (runs the bot as worker)
CMD ["python", "crypto_bot.py"]
