from fastapi import APIRouter, HTTPException
from app.api.v1.schemas.scraping import ScrapeRequest
from app.services.task_manager import send_scrape_task
from app.extensions import redis_client

import logging
import json

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("")
def enqueue_scrape(request: ScrapeRequest):
    try:
        task = send_scrape_task(request.cnpj)
        task_id = task.id

        redis_client.setex(task_id, 3600, json.dumps({"status": "pending"}))
        logger.info(f"T01 Task enfileirada, status: 'pending', task_id: {task_id}")

        return {"message": "Tarefa enviada com sucesso", "task_id": task_id}

    except Exception as e:
        logger.error(f"Erro ao enfileirar tarefa: {e}")
        raise HTTPException(status_code=500, detail="Erro ao enfileirar tarefa.")
