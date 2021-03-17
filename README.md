# FastAPI Celery MQ Example

## Running with Docker
```bash
docker-compose build
docker-compose up
```

## Running without Docker
```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```
```bash
celery --app worker.celery_app worker -c 2 --loglevel=info
```