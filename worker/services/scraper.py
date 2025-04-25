import re
import time
import logging
import unicodedata
from enum import Enum

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from worker.loader import SINEGRA_URL

logger = logging.getLogger(__name__)


class ScraperStatus(str, Enum):
    SUCCESS = "success"
    NOT_FOUND = "not_found"
    INVALID = "invalid"

    NOT_FOUND_MSG = "Não foi encontrado nenhum contribuinte para o parâmetro informado!"
    INVALID_MSG = "CNPJ Inválido!"
    REDIRECT_ERROR_MSG = "Ocorreu um erro ao processar a requisição. A página não redirecionou como esperado."


class CnpjScraper:
    def __init__(self, cnpj: str, task_id: str):
        self.url = SINEGRA_URL
        self.cnpj = cnpj
        self.task_id = task_id


    def _start_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920x1080")
        return webdriver.Chrome(options=options)
    

    def is_redirected(self, current_url: str) -> bool:
        return current_url.rstrip("/") != self.url.rstrip("/")


    def _normalize(self, value: str) -> str:
        if not value:
            return value

        cleaned = re.sub(r"\s+", " ", value)
        return unicodedata.normalize("NFKC", cleaned).strip()


    def _extract_field(self, soup: BeautifulSoup, label: str) -> str:
        span = soup.find("span", string=lambda text: text and label in text)
        if span:
            next_sibling = span.find_next_sibling("span")
            if next_sibling:
                return self._normalize(next_sibling.get_text())
        return None


    def _extract_div_field(self, soup: BeautifulSoup, label: str) -> str:
        div = soup.find("div", string=lambda text: text and label in text)
        if div:
            next_sibling = div.find_next_sibling("span")
            if next_sibling:
                return self._normalize(next_sibling.get_text())
        return None


    def _extract_main_activity(self, soup: BeautifulSoup) -> str:
        label = soup.find("span", string=lambda t: t and "Atividade Principal" in t)
        if label:
            atividade = label.find_next("span", class_="label_text")
            if atividade:
                return self._normalize(atividade.get_text())
        return None
    

    def _extract_all_fields(self, soup: BeautifulSoup) -> dict:
        return {
            "cnpj": self.cnpj,
            "razao_social": self._extract_field(soup, "Nome Empresarial"),
            "nome_fantasia": self._extract_field(soup, "Nome Fantasia"),
            "ie": self._extract_field(soup, "Inscrição Estadual"),
            "regime": self._extract_field(soup, "Regime de Apuração"),
            "situacao": self._extract_field(soup, "Situação Cadastral Vigente"),
            "unidade_auxiliar": self._extract_field(soup, "Unidade Auxiliar:"),
            "condicao_uso": self._extract_field(soup, "Condição de Uso:"),
            "data_final_contrato": self._extract_field(soup, "Data Final de Contrato:"),
            "data_cadastramento": self._extract_field(soup, "Data de Cadastramento:"),
            "data_situacao": self._extract_field(soup, "Data desta Situação Cadastral:"),
            "operacoes_nf": self._extract_field(soup, "Operações com NF-E:"),
            "atividade_principal": self._extract_main_activity(soup),
            "data_consulta": self._extract_field(soup, "Data da Consulta"),
            "endereco": self._extract_div_field(soup, "Endereço Estabelecimento")
        }


    def run(self) -> dict:
        logger.info(f"W01 - Iniciando scraping para CNPJ: {self.cnpj}, task_id: {self.task_id}")
        driver = self._start_driver()

        try:
            driver.get(self.url)
            time.sleep(1)

            driver.find_element(By.ID, "rTipoDocCNPJ").click()

            field = driver.find_element(By.ID, "tCNPJ")
            field.clear()
            field.send_keys(self.cnpj)

            driver.find_element(By.NAME, "btCGC").click()

            # Verificação de CNPJ válido
            boxes = driver.find_elements(By.CLASS_NAME, "zion_rich_validation_box_show")
            for box in boxes:
                text = box.text.strip()
                if ScraperStatus.INVALID_MSG.value.lower() in text.lower():
                    logger.warning(f"W01 - CNPJ inválido detectado dinamicamente, task_id: {self.task_id}")
                    return {
                        "status": ScraperStatus.INVALID.value,
                        "message": ScraperStatus.INVALID_MSG.value,
                        "cnpj": self.cnpj
                    }

            # Verificação de erro no redirecionamento
            if not self.is_redirected(driver.current_url):
                logger.error(f"W01 - CNPJ {self.cnpj} Página não redirecionou após consulta. task_id: {self.task_id}")
                raise RuntimeError(ScraperStatus.REDIRECT_ERROR_MSG.value)
            
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            # Verificação se retonar dados para o CNPJ
            message = soup.find("div", string=lambda text: text and ScraperStatus.NOT_FOUND_MSG.lower() in text.lower())
            if message:
                logger.warning(f"W01 - CNPJ {self.cnpj} não retornou dados na consulta. task_id: {self.task_id}")
                return {
                    "status": ScraperStatus.NOT_FOUND.value,
                    "cnpj": self.cnpj,
                    "message": ScraperStatus.NOT_FOUND_MSG.value
                }


            extracted_data = self._extract_all_fields(soup)
            logger.info(f"W01 - Dados extraídos com sucesso para {self.cnpj}, task_id: {self.task_id}")
            return {
                "status": ScraperStatus.SUCCESS.value,
                **extracted_data
            }
        
        except Exception as e:
            logger.exception(f"W01 - Erro inesperado ao processar o CNPJ {self.cnpj}, task_id: {self.task_id}")
            raise e

        finally:
            driver.quit()
