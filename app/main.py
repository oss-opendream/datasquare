'''Initializes the FastAPI Application.'''


import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette import status

from app.models.database import Base, datasquare_db
from app.routers import feed, data_request, issue_comment, sign, database_router, profile, admin
from app.utils.errer_handlers import error_handlers


from app.schemas.user_schema import User, AdminUser
from app.utils.get_current_user import get_current_user

templates = Jinja2Templates(directory='app/templates')


def create_app():
    '''
    FastAPI app 객체를 생성합니다.
    - 'static' 디렉터리의 파일들을 '/static'으로 라우팅
    - 모든 라우터를 app에 포함
    :return: FastAPI app 객체
    '''

    Base.metadata.create_all(bind=datasquare_db.engine, checkfirst=True)

    created_app = FastAPI(title='Datasquare',
                          description='데이터 협업을 위한 조직 간 커뮤니케이션 플랫폼',
                          lifespan=admin.lifespan)

    created_app.mount(
        '/static', StaticFiles(directory='app/static'), name='static')

    routers = [
        sign.router,
        feed.router,
        data_request.data_request_router,
        issue_comment.issue_comment_router,
        database_router.router,
        profile.profilerouter,
        admin.router,
    ]

    for router in routers:
        created_app.include_router(router)

    for status_code, handler in error_handlers.items():
        created_app.add_exception_handler(status_code, handler)

    return created_app


app = create_app()


@app.middleware("http")
async def admin_middleware(request: Request, call_next):

    if getattr(app, 'redirect_flag', False):
        app.redirect_flag = False
        return RedirectResponse(url="/admin/account/create", status_code=status.HTTP_302_FOUND)

    response = await call_next(request)

    return response


@app.get('/')
def root_redirect(request: Request):
    '''
    루트 라우터 함수
    '''
    try:
        current_user = get_current_user(request)
        if isinstance(current_user, User):
            return RedirectResponse('/feed', status_code=status.HTTP_302_FOUND)
        elif isinstance(current_user, AdminUser):
            return RedirectResponse('/admin', status_code=status.HTTP_302_FOUND)

    except:
        return RedirectResponse('/signin', status_code=status.HTTP_302_FOUND)


@app.get('/databases')
def databases_test():
    return {'hello': 'world'}


if __name__ == '__main__':

    uvicorn.run('main:app',
                host='0.0.0.0', port=8000, reload=True)
