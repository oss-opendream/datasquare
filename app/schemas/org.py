from pydantic import BaseModel


class DBConnectionForm(BaseModel):
    host: str
    port: int
    db_name: str
    user: str
    password: str
