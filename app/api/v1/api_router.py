from fastapi import APIRouter

from app.api.v1.routes import scraping, results

router = APIRouter()
router.include_router(scraping.router, prefix="/scrape", tags=["Scraping"])
router.include_router(results.router, prefix="/results", tags=["Results"])