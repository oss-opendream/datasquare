from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/issue/publish", response_class=HTMLResponse)
async def issue_publish(request: Request):
    return templates.TemplateResponse(
        request=request, name="issue_publish.html"
    )