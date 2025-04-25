import logging

from worker.services.scraper import CnpjScraper

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    cnpj = "00.006.486/0001-75"   # Valido
    # cnpj = "84.911.098/0001-29"   # Valido sem registro 
    # cnpj = "12.345.678/0001-93"   # Inválido

    task_id = "manual-test-001"

    scraper = CnpjScraper(cnpj=cnpj, task_id=task_id)
    result = scraper.run()

    print("Resultado final do scraping:")
    print(result)
