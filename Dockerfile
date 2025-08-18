# Secure, minimal image for Streamlit
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8501

WORKDIR /app

# System deps only while building wheels, then purge
COPY requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/*

# App code
COPY . /app

# Default Streamlit config (XSRF/CORS, no telemetry)
RUN mkdir -p /app/.streamlit
COPY .streamlit/config.toml /app/.streamlit/config.toml

# Non-root user
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8501

# Healthcheck (works in many platforms)
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -fsS http://127.0.0.1:${PORT}/_stcore/health || exit 1

# If your main is streamlit_app.py, keep it here:
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=${PORT}", "--server.address=0.0.0.0"]
