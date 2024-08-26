'''Initializes the FastAPI Application.'''


from fastapi import FastAPI

from app.routers import org
from app.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(org.router)


@app.get('/')
def read_root():
    return {'hello': 'world'}
