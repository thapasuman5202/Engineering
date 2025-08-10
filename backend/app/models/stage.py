from pydantic import BaseModel
from typing import Any, Optional

class StageResult(BaseModel):
    stage: int
    status: str
    data: Optional[Any] = None
