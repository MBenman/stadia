#Build
FROM python:3.13.6-slim AS builder

RUN mkdir /app

WORKDIR /app

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

ENV DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,0.0.0.0"

RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

#Production
FROM python:3.13.6-slim

# RUN useradd -m -r appuser && \
#   mkdir /app && \
#   chown -R appuser /app

RUN mkdir /app

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# WORKDIR /app

# COPY --chown=appuser:appuser . .
COPY . /app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,0.0.0.0"

# USER appuser
EXPOSE 8000
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "stadiapi.wsgi:application"]

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use ENTRYPOINT instead of CMD for GitHub Actions
ENTRYPOINT ["/entrypoint.sh"]