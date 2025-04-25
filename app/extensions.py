from redis import Redis
from celery import Celery
from app.loader import REDIS_URL, RABBITMQ_URL

# ===================
# Redis Client
# ===================
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)


# ===================
# Celery App
# ===================
celery_app = Celery("python_teste")

celery_app.conf.update(
    broker_url=RABBITMQ_URL,
    result_backend=REDIS_URL,
    task_routes={
        # Adicionar aqui demais relação task - fila
        "scrape_cnpj_task": {"queue": "scrape_cnpj_task"},
    },
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
