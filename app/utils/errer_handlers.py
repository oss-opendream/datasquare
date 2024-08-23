from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

templates = Jinja2Templates(directory='app/templates')


async def not_found_error(request: Request, exc: Exception):
    
    ret = templates.TemplateResponse(
        'pages/edd',
        {
            "request": request,
            "status_code": 403,
            "error_message": "Access Forbidden",
        },
        status_code=403
    )

    return ret

# 다른 오류 핸들러들을 여기에 추가할 수 있습니다.
async def internal_server_error(request: Request, exc: Exception):
    return templates.TemplateResponse(
        status_code=401,
        content={"message": "Internal Server Error"}
    )

async def context_must_include(request: Request, exc: Exception):
        return templates.TemplateResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )

# 모든 오류 핸들러를 딕셔너리로 관리
error_handlers = {
    404: not_found_error,
    500: internal_server_error,
    # 필요한 다른 오류 코드와 핸들러를 여기에 추가
}