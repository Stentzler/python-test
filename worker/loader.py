import os
from dotenv import load_dotenv

load_dotenv()

SINEGRA_URL = os.getenv("SINEGRA_URL", 'http://appasp.sefaz.go.gov.br/Sintegra/Consulta/default.html')
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672//")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
