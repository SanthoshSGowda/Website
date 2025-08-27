FROM python:3.13.2-slim-bookworm

WORKDIR /app

# 1) update & minimal build deps (patches OS libs)
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc curl && \
    rm -rf /var/lib/apt/lists/*

# 2) copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) copy app source
COPY . .

# 4) add a lightweight healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD curl -f http://127.0.0.1:5000/ || exit 1

EXPOSE 5000
CMD ["python", "-m", "app.app"]
