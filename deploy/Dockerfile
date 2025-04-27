# Stage 1: Base build stage
FROM python:3.13-slim AS builder
 
# Create the app directory
RUN mkdir /finance
 
# Set the working directory
WORKDIR /finance
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip and install dependencies
RUN pip install --upgrade pip 
 
# Copy the requirements file first (better caching)
COPY ../requirements.txt /finance/
 
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
 
# Stage 2: Production stage
FROM python:3.13-slim
 
RUN useradd -m -r appuser && \
   mkdir /finance && \
   chown -R appuser /finance
 
# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
# Set the working directory
WORKDIR /finance
 
# Copy application code
COPY --chown=appuser:appuser ./finance/ .
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Set the DJANGO_SETTINGS_MODULE environment variable
ENV DJANGO_SETTINGS_MODULE=finance.settings

# Switch to non-root user
USER appuser
 
# Expose the application port
EXPOSE 8000 
 
# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "finance.wsgi:application"]