from fastapi.testclient import TestClient as FastAPITestClient
from unittest.mock import patch

from app.main import app

client = FastAPITestClient(app)

@patch("app.api.v1.routes.results.redis_client.get")
def test_get_result_not_found(mock_redis_get):
    mock_redis_get.return_value = None

    response = client.get("/api/v1/results/task-id-nao-existe")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Nenhuma informação encontrada para o task_id: task-id-nao-existe"
    }


@patch("app.api.v1.routes.results.redis_client.get")
def test_get_result_pending(mock_redis_get):
    mock_redis_get.return_value = '{"status": "pending"}'

    response = client.get("/api/v1/results/task-pendente-001")
    assert response.status_code == 200
    assert response.json() == {
        "task_id": "task-pendente-001",
        "status": "pending",
        "data": None
    }


@patch("app.api.v1.routes.results.redis_client.get")
def test_get_result_done(mock_redis_get):
    mock_redis_get.return_value = '{"status": "success", "cnpj": "00.006.486/0001-75", "razao_social": "Exemplo"}'

    response = client.get("/api/v1/results/task-ok-001")
    assert response.status_code == 200
    assert response.json() == {
        "task_id": "task-ok-001",
        "status": "done",
        "data": {
            "status": "success",
            "cnpj": "00.006.486/0001-75",
            "razao_social": "Exemplo"
        }
    }
