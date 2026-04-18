# Use Python 3.11 with full system tools
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Set working directory
WORKDIR /app

# Install system dependencies required by Playwright browsers
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (without --with-deps since we installed deps manually)
RUN python -m playwright install chromium firefox

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
