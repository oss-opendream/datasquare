
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from starlette import status
from contextlib import asynccontextmanager

from app.crud.user_crud import UserData
from app.crud.team_crud import TeamData
from app.schemas import user_schema
from app.utils.get_current_user import get_current_user

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory='app/templates')


@asynccontextmanager
async def lifespan(app: FastAPI):
    # When service starts.

    admin = UserData()

    if not admin.is_admin_table():
        app.redirect_flag = True
        app.setting_tema = False  # 첫 요청에 리다이렉션 플래그 설정
    else:
        app.redirect_flag = False

    yield


@router.get('')
async def redirect_admin(current_user=Depends(get_current_user)):

    if isinstance(current_user, user_schema.AdminUser):
        return RedirectResponse(url='/admin/teams', status_code=status.HTTP_302_FOUND)

    else:
        raise HTTPException(status_code=401)


@router.get("/account/create")
async def create_admin(request: Request):

    if not UserData().is_admin_table():
        return templates.TemplateResponse("pages/admin_signup.html",
                                          {'request': request}
                                          )
    else:
        raise HTTPException(status_code=401)


@router.post("/account/create")
async def create_admin_post(email=Form(...),
                            name=Form(...),
                            password=Form(...),
                            ):

    UserData().create_admin_re(email=email,
                               name=name,
                               password=password)

    return RedirectResponse(url="/signin", status_code=status.HTTP_302_FOUND)


@router.get("/teams")
async def teams_settings(request: Request,
                         current_user=Depends(get_current_user),
                         ):

    if isinstance(current_user, user_schema.AdminUser):
        return templates.TemplateResponse(
            'pages/team_create.html',
            {
                'request': request
            }
        )

    else:
        raise HTTPException(status_code=401)


@router.post("/teams/set")
async def set_teams(team_names: list[str] = Form(...),
                    current_user=Depends(get_current_user),
                    ):

    if isinstance(current_user, user_schema.AdminUser):
        teamdata = TeamData()
        teamdata.create_teams(team_names=team_names)

        return RedirectResponse(url="/admin/teams", status_code=status.HTTP_302_FOUND)

    else:
        raise HTTPException(status_code=401)
