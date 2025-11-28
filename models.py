from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Calculation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    a: int
    b: int
    result: int
    name: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)