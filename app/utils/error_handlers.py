'''error 페이지 및 메시지를 처리하는 모듈'''


from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='app/templates')


async def bad_request(request: Request):
    '''404 Bad_Request 오류 대응 페이지 및 오류 메시지를 출력하는 함수'''

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': 400,
            'error_message': 'Bad_Request',
        },
        status_code=400
    )


async def unauthorized(request: Request):
    '''401 Unauthorized 오류 대응 페이지 및 오류 메시지를 출력하는 함수'''

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': 401,
            'error_message': 'Unauthorized',
        },
        status_code=401
    )


async def forbidden(request: Request):
    '''403 Forbidden 오류 대응 페이지 및 오류 메시지를 출력하는 함수'''

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': 403,
            'error_message': 'Forbidden',
        },
        status_code=403
    )


async def not_found(request: Request):
    '''404 Not_Found 오류 대응 페이지 및 오류 메시지를 출력하는 함수'''

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': 404,
            'error_message': 'Not_Found',
        },
        status_code=404
    )


async def unprocessable_entity(request: Request):
    '''422 Unprocessable_Entity 오류 대응 페이지 및 오류 메시지를 출력하는 함수'''

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': 422,
            'error_message': 'Unprocessable_Entity',
        },
        status_code=422
    )


async def internal_server_error(request: Request):
    '''500 Internal_Server_Error 오류 대응 페이지 및 오류 메시지를 출력하는 함수'''

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': 500,
            'error_message': 'Internal_Server_Error',
        },
        status_code=500
    )


error_handlers = {
    400: bad_request,
    401: unauthorized,
    403: forbidden,
    404: not_found,
    422: unprocessable_entity,
    500: internal_server_error,
}
