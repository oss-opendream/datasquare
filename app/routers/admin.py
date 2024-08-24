
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

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')
router = APIRouter(prefix="/profile")

router = APIRouter(prefix="/admin")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # When service starts.

    admin = UserData()

    if not admin.is_admin_table():
        app.redirect_flag = True
        app.setting_tema = False  # 첫 요청에 리다이렉션 플래그 설정
    else:
        app.redirect_flag = False

    # admin.create_admin_re()

    yield


@router.get("/")
async def create_admin(request: Request):
    if UserData().is_admin_table():
        current_user = get_current_user(request)
        if isinstance(current_user, user_schema.AdminUser):
            return RedirectResponse(url="/admin",  status_code=status.HTTP_302_FOUND)
        else:
            raise HTTPException(status_code=401)

    else:
        return templates.TemplateResponse("pages/admin_signup.html",
                                          {'request': request})


@router.post("/")
async def create_admin_post(email=Form(...),
                            name=Form(...),
                            password=Form(...),
                            ):

    UserData().create_admin_re(email=email,
                               name=name,
                               password=password)

    return RedirectResponse(url="/signin",  status_code=status.HTTP_302_FOUND)


@router.get("/init")
async def admin_settings(request: Request,
                         current_user=Depends(get_current_user),
                         ):

    # 일반 계정인지 확인
    if isinstance(current_user, user_schema.User):
        return RedirectResponse(url="/signin")

    else:
        return templates.TemplateResponse(
            'pages/team_create.html',
            {
                'request': request
            }
        )


@router.post("/init/set_teams")
async def set_teams_profile(team_names: list[str] = Form(...),
                            current_user=Depends(get_current_user),
                            ):
    print(team_names)
    # 일반 계정인지 확인
    if isinstance(current_user, user_schema.User):
        return RedirectResponse(url="/signin")

    else:
        teamdata = TeamData()
        teamdata.create_teams(team_names=team_names)

        return RedirectResponse('/admin/init', status_code=status.HTTP_302_FOUND)
