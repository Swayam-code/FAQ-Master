# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=faqmaster.settings_prod

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy project
COPY . /app/

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/mediafiles

# Create and switch to non-root user
RUN useradd -m myuser
RUN chown -R myuser:myuser /app
USER myuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "python manage.py collectstatic --noinput && exec gunicorn faqmaster.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
