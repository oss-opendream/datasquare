from pydantic import BaseModel
from typing import Optional


class DBConnectionForm(BaseModel):
    host: str
    port: int
    db_name: str
    user: str
    password: Optional[str] = None
