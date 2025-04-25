from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Union, Dict

class TaskStatus(str, Enum):
    pending = "pending"
    done = "done"
    error = "error"

class TaskResultResponse(BaseModel):
    task_id: str
    status: TaskStatus = Field(..., example="done")
    data: Optional[Union[Dict, str]] = None

class ErrorResponse(BaseModel):
    detail: str = Field(..., example="Nenhuma informação encontrada para o task_id: ")