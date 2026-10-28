FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Ho_Chi_Minh

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    tzdata \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "muse_seo_daemon.py", "--mode", "daemon", "--daily-time", "07:00", "--watch-interval", "900"]
