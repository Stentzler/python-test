from celery import Celery
from redis import Redis

from worker.loader import RABBITMQ_URL, REDIS_URL

celery_app = Celery("python_worker", broker=RABBITMQ_URL, backend=REDIS_URL)

redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
