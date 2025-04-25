import os
from dotenv import load_dotenv

load_dotenv(override=True)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672//")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")