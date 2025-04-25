from app.extensions import celery_app

def send_scrape_task(cnpj: str):
    task = celery_app.send_task("scrape_cnpj_task", args=[cnpj])
    return task