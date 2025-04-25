import logging
from fastapi import FastAPI

from app.api.v1.api_router import router as api_v1_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="python-teste API")

app.include_router(api_v1_router, prefix="/api/v1")