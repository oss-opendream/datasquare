import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import feed


def create_app() -> None:
    """
    FastAPI app 객체를 생성합니다.
    - 'static' 디렉터리의 파일들을 '/static'으로 라우팅
    - 모든 라우터를 app에 포함
    :return: FastAPI app 객체
    """
    created_app = FastAPI(title="Datasquare",
                          description="데이터 협업을 위한 조직 간 커뮤니케이션 플랫폼")

    created_app.mount(
        "/static", StaticFiles(directory="static"), name="static")

    created_app.include_router(feed.router)

    return created_app


app = create_app()


@app.get('/')
def read_root():
    """
    루트 라우터 함수
    """
    return {'hello': 'world'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, reload=True)
