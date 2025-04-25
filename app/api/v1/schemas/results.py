from enum import Enum
from pydantic import BaseModel
from typing import Optional, Union, Dict

class TaskStatus(str, Enum):
    pending = "pending"
    done = "done"
    error = "error"

class TaskResultResponse(BaseModel):
    task_id: str
    status: TaskStatus
    data: Optional[Union[Dict, str]] = None
