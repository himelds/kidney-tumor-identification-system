# Railway Deployment

## Web Service

Railway can deploy the FastAPI API from the repository root using Nixpacks.

Start command:

```bash
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

Health check path:

```text
/api/v1/health
```

## Required Variables

Set these variables in Railway:

```env
APP_NAME=Kidney Tumor Identification System
APP_VERSION=0.1.0
API_PREFIX=/api/v1
LOG_LEVEL=INFO
DEBUG=False
HF_MODEL_REPO=Himel000/kidney-tumor-efficientnetb4
HF_MODEL_FILENAME=model.keras
MODEL_IMAGE_SIZE=380
UNCERTAINTY_THRESHOLD=0.3
DATABASE_PATH=data/predictions.db
MAX_UPLOAD_SIZE_MB=10
TEMP_DIR=temp/uploads
REDIS_URL=${{Redis.REDIS_URL}}
```

Add a Railway Redis service and connect `REDIS_URL` from that service.

## Celery Worker

Async PDF report generation needs a separate Railway service using the same repo
and variables as the web service.

Worker start command:

```bash
celery -A api.workers.celery_app.celery_app worker --loglevel=info
```

## Notes

Railway disk is ephemeral. SQLite prediction history and generated report files
will not persist across redeploys unless you attach persistent storage or move
those artifacts to an external service.
