'''error 페이지 및 메시지를 처리하는 모듈'''


from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='app/templates')


async def error_catch(request: Request, exc: Exception):
    '''에러 처리 페이지 함수'''

    return templates.TemplateResponse(
        'pages/404.html',
        {
            'request': request,
            'status_code': exc.status_code,
            'error_message': exc.detail,
        },
    )


error_handlers = {
    400: error_catch,
    401: error_catch,
    402: error_catch,
    403: error_catch,
    404: error_catch,
    405: error_catch,
    406: error_catch,
    407: error_catch,
    408: error_catch,
    409: error_catch,
    410: error_catch,
    411: error_catch,
    412: error_catch,
    413: error_catch,
    414: error_catch,
    415: error_catch,
    416: error_catch,
    417: error_catch,
    426: error_catch,
    428: error_catch,
    429: error_catch,
    431: error_catch,
    451: error_catch,
    500: error_catch,
    501: error_catch,
    502: error_catch,
    503: error_catch,
    504: error_catch,
    505: error_catch,
    506: error_catch,
    507: error_catch,
    508: error_catch,
    510: error_catch,
}
