from celery import Celery
from app.config import settings

# Команда для запуска celery:
# celery -A app.tasks.celery_config:celery worker --loglevel=INFO --pool=solo (запускается в отдельном cmd)

# Команда для запуска flower:
# celery -A app.tasks.celery_config:celery flower (запускается в отдельном cmd)


celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.tasks.tasks"]
)