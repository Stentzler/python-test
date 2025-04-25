import pytest
from fastapi.testclient import TestClient as FastAPITestClient
from unittest.mock import patch

from app.main import app

client = FastAPITestClient(app)


@patch("app.api.v1.routes.scraping.redis_client.setex")
@patch("app.api.v1.routes.scraping.send_scrape_task")
def test_enqueue_scrape_success(mock_send_task, mock_redis_setex):
    mock_send_task.return_value.id = "mock-task-id-123"
    mock_redis_setex.return_value = True

    response = client.post("/api/v1/scrape", json={"cnpj": "00.006.486/0001-75"})

    assert response.status_code == 200
    assert response.json() == {
        "message": "Tarefa enviada com sucesso",
        "task_id": "mock-task-id-123"
    }
    mock_send_task.assert_called_once()
    mock_redis_setex.assert_called_once()


@pytest.mark.parametrize("cnpj", [
    "123",                         # Não possui 14 digitos
    "00.000.000/0000-00",          # formato válido, mas dígitos incorretos
    "abcdefghijklmno",             # letras
    "11111111111111",              # CNPJ inválido por padrão
])
def test_enqueue_scrape_invalid_cnpj(cnpj):
    response = client.post("/api/v1/scrape", json={"cnpj": cnpj})
    assert response.status_code == 422
    assert "CNPJ inválido" in response.json()["detail"][0]["msg"]
