import logging, json
from fastapi import APIRouter, HTTPException

from app.extensions import redis_client

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/{task_id}")
def get_scrape_result(task_id: str):    
    result = redis_client.get(task_id)
    if result is None:
        logger.warning(f"T02 Nenhuma informação encontrada para task_id: {task_id}")
        raise HTTPException(
            status_code=404,
            detail=f"Nenhuma informação encontrada para o task_id: {task_id}"
        )

    parsed = json.loads(result) if result else None
    if parsed.get("status") == "pending":
        logger.info(f"T02 Resultado pendente para task_id: {task_id}")
        return {"task_id": task_id, "status": "pending", "data": None}

    logger.info(f"T02 Resultado retornado para task_id: {task_id}")
    return {"task_id": task_id, "status": "done", "data": parsed}
