import pytest
from unittest.mock import patch, MagicMock
from worker.services.scraper import CnpjScraper, ScraperStatus


@patch("worker.services.scraper.webdriver.Chrome")
def test_run_success(mock_chrome):
    driver = MagicMock()
    mock_chrome.return_value = driver

    driver.current_url = "http://appasp.sefaz.go.gov.br/Sintegra/Consulta/consultar.asp"
    driver.page_source = '''
        <html>
            <span class="label_title">Nome Empresarial</span>
            <span class="label_text">Empresa Exemplo Ltda</span>
        </html>
    '''

    scraper = CnpjScraper("00.006.486/0001-75", "mock-task-id")
    result = scraper.run()

    assert result["status"] == ScraperStatus.SUCCESS
    assert result["razao_social"] == "Empresa Exemplo Ltda"


@patch("worker.services.scraper.webdriver.Chrome")
def test_run_not_found(mock_chrome):
    driver = MagicMock()
    mock_chrome.return_value = driver

    driver.current_url = "http://appasp.sefaz.go.gov.br/Sintegra/Consulta/consultar.asp"
    driver.page_source = '''
        <html>
            <div>Não foi encontrado nenhum contribuinte para o parâmetro informado!</div>
        </html>
    '''

    scraper = CnpjScraper("84.911.098/0001-29", "mock-task-id")
    result = scraper.run()

    assert result["status"] == ScraperStatus.NOT_FOUND


@patch("worker.services.scraper.webdriver.Chrome")
def test_run_invalid(mock_chrome):
    driver = MagicMock()
    mock_chrome.return_value = driver

    fake_error_div = MagicMock()
    fake_error_div.text = "CNPJ Inválido!"
    driver.find_elements.return_value = [fake_error_div]

    driver.current_url = "http://appasp.sefaz.go.gov.br/Sintegra/Consulta/default.html"

    scraper = CnpjScraper("12.345.678/0001-93", "mock-task-id")
    result = scraper.run()

    assert result["status"] == ScraperStatus.INVALID


@patch("worker.services.scraper.webdriver.Chrome")
def test_run_redirect_error(mock_chrome):
    driver = MagicMock()
    mock_chrome.return_value = driver

    driver.current_url = "http://appasp.sefaz.go.gov.br/Sintegra/Consulta/default.html"
    driver.page_source = "<html></html>"

    scraper = CnpjScraper("00.006.486/0001-75", "mock-task-id")

    with pytest.raises(RuntimeError, match=ScraperStatus.REDIRECT_ERROR_MSG.value):
        scraper.run()


@patch("worker.services.scraper.webdriver.Chrome")
def test_run_exception(mock_chrome):
    mock_chrome.side_effect = Exception("Driver failed")

    scraper = CnpjScraper("00.006.486/0001-75", "mock-task-id")

    with pytest.raises(Exception, match="Driver failed"):
        scraper.run()