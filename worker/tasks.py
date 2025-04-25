import json
import logging

from worker.extensions import celery_app, redis_client
from worker.services.scraper import CnpjScraper

logger = logging.getLogger(__name__)

@celery_app.task(
    name="scrape_cnpj_task",
    queue="scrape_cnpj_task",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=120,
    retry_kwargs={"max_retries": 3},
    retry_jitter=True
)
def scrape_cnpj_task(self, cnpj: str):
    task_id = self.request.id
    current_try = self.request.retries
    max_retries = self.max_retries
    is_last_retry = current_try >= max_retries

    logger.info(f"W01 - Worker recebeu task para CNPJ: {cnpj}, task: {task_id}")

    try:
        result = CnpjScraper(cnpj, task_id).run()
        redis_client.setex(task_id, 3600, json.dumps(result))
        logger.info(f"W01 - Resultado salvo no Redis com task_id={task_id}")

    except Exception as e:
        logger.error(f"W01 - Erro ao processar task_id={task_id}: {e}")
        redis_client.setex(task_id, 3600, json.dumps({
            "status": "error",
            "message": str(e),
            "retrying": not is_last_retry,
            "attempt": current_try + 1
        }))
        raise e
