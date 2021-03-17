# FastAPI Celery MQ Example

Distributed task queue with Celery and RabbitMQ example.

This example has both of the worker and broker in the same codebase, it is possible to split the codebase.

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
