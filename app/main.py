import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import issue_publish



def create_app():
    app = FastAPI()

    # css, js, images 넣는 폴더 마운트
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # 라우터 포함시키기
    app.include_router(issue_publish.router)


    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)