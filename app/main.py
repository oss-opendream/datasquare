'''Initializes the FastAPI Application.'''


import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def create_app():
    app = FastAPI()
    # Base.metadata.create_all(bind=engine)

    # css, js, images 넣는 폴더 마운트
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # 각자 라우터 추가 ex) app.include_router(~.router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1",
                port=8000, reload=True, workers=1)
