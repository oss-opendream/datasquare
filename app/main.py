'''Initializes the FastAPI Application.'''


import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.models.database import Base, datasquare_db
from app.crud.user_crud import UserData
from app.routers import feed, issue_publish, issue_view, sign, database_router, profile, admin
# from app.utils.errer_handlers import error_handlers

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


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
        issue_publish.router,
        issue_view.router,
        database_router.router,
        profile.router,
        admin.router,
    ]

    for router in routers:
        created_app.include_router(router)

    return created_app


app = create_app()


@app.middleware("http")
async def admin_middleware(request: Request, call_next):

    if getattr(app, 'redirect_flag', False):
        app.redirect_flag = False
        return RedirectResponse(url="/admin")

    response = await call_next(request)

    return response


@app.get('/')
def read_root():
    '''
    루트 라우터 함수
    '''
    return {'hello': 'world'}


@app.get('/databases')
def databases_test():
    return {'hello': 'world'}


# 사용자 정의 HTTP 예외 핸들러
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("pages/404.html", {"request": request, "message": "An HTTP error occurred: " + exc.detail}, status_code=exc.status_code)

# 검증 오류 핸들러 (예: 잘못된 입력 데이터)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse("pages/404.html", {"request": request, "message": "Validation error: " + str(exc)}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

# 일반 예외 핸들러 (모든 예외 처리)
@app.exception_handler(RequestValidationError)
async def custom_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse("pages/404.html", {"request": request, "message": "An unexpected error occurred: " + str(exc)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/cause_error/")
async def cause_error():
    raise RuntimeError("This is a test error!")

# for status_code, handler in error_handlers.items():
#     app.add_exception_handler(status_code, handler)





if __name__ == '__main__':

    uvicorn.run('main:app',
                host='0.0.0.0', port=8000, reload=True)

