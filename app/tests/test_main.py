import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models.database import Base, datasquare_db
from app.crud.user_crud import UserData
from app.routers import feed, issue_publish, issue_view, sign, database_router

templates = Jinja2Templates(directory='app/templates')


def create_app() -> None:
    '''
    FastAPI app 객체를 생성합니다.
    - 'static' 디렉터리의 파일들을 '/static'으로 라우팅
    - 모든 라우터를 app에 포함
    :return: FastAPI app 객체
    '''
    created_app = FastAPI(title='Datasquare',
                          description='데이터 협업을 위한 조직 간 커뮤니케이션 플랫폼')

    created_app.mount(
        '/static', StaticFiles(directory='app/static'), name='static')

    routers = [
        sign.router,
        feed.router,
        issue_publish.router,
        issue_view.router,
        database_router.router,
    ]

    for router in routers:
        created_app.include_router(router)

    return created_app


app = create_app()


@app.get('/')
def read_root():
    '''
    루트 라우터 함수
    '''
    return {'hello': 'world'}


@app.get('/databases')
def databases_test():
    return {'hello': 'world'}


@app.get('/404')
def not_found_error(request: Request):
    return templates.TemplateResponse(
        'pages/404.html', {"request": request}
    )


@app.on_event("startup")
async def on_startup():

    admin = UserData()
    if not admin.get_user('admin@admin.com', key='email'):
        admin.create_admin()

if __name__ == '__main__':
    Base.metadata.create_all(bind=datasquare_db.engine, checkfirst=True)

    uvicorn.run('app.tests.test_main:app',
                host='0.0.0.0', port=8001, reload=True)
