# Use Python 3.11 as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies first
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers with system dependencies
# Note: playwright command is now available after pip install
RUN python -m playwright install --with-deps chromium firefox

# Copy framework code and tests
COPY framework/ ./framework/
COPY tests/ ./tests/
COPY conftest.py .
COPY config.yaml .
COPY config.skechers-staging.yaml .
COPY pytest.ini .

# Create reports directory
RUN mkdir -p reports/screenshots reports/traces

# Set default command to run pytest
CMD ["pytest", "--headless"]
