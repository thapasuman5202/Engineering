FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir celery[redis]
COPY . ./workers
CMD ["celery", "-A", "workers", "worker", "--loglevel=info"]
