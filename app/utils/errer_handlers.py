from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

templates = Jinja2Templates(directory='app/templates')


async def Bad_Request(request: Request, exc: Exception):

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': 400,
            'error_message': 'Bad_Request',
        },
        status_code=400
    )

async def Unauthorized(request: Request, exc: Exception):

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': 401,
            'error_message': 'Unauthorized',
        },
        status_code=401
    )

async def Forbidden(request: Request, exc: Exception):

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': 403,
            'error_message': 'Forbidden',
        },
        status_code=403
    )

async def Not_Found(request: Request, exc: Exception):

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': 404,
            'error_message': 'Not_Found',
        },
        status_code=404
    )

async def Unprocessable_Entity(request: Request, exc: Exception):

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': 422,
            'error_message': 'Unprocessable_Entity',
        },
        status_code=422
    )

async def Internal_Server_Error(request: Request, exc: Exception):

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': 500,
            'error_message': 'Internal_Server_Error',
        },
        status_code=500
    )


# 모든 오류 핸들러를 딕셔너리로 관리
error_handlers = {
    400: Bad_Request,
    401: Unauthorized,
    403: Forbidden,
    404: Not_Found,
    422: Unprocessable_Entity,
    500: Internal_Server_Error,
}