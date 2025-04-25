from unittest.mock import patch
from app.services.task_manager import send_scrape_task

@patch("app.services.task_manager.celery_app.send_task")
def test_send_scrape_task(mock_send_task):
    mock_send_task.return_value.id = "fake-id"

    result = send_scrape_task("00.006.486/0001-75")
    
    assert result.id == "fake-id"
    mock_send_task.assert_called_once()
