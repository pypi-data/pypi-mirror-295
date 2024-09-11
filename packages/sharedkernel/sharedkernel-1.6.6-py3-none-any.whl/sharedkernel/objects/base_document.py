from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BaseDocument(BaseModel):
    id: Optional[str]
    is_deleted: bool = False
    created_on: datetime = datetime.now()
