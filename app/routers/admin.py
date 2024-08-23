import os
import base64
from dotenv import load_dotenv
from datetime import timedelta, datetime
from typing import Annotated

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, Depends, Form, HTTPException, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi import Cookie, Response
from jose import jwt
from starlette import status
from contextlib import asynccontextmanager

from app.crud.user_crud import UserData
from app.crud.team_crud import TeamData
from app.schemas import user_schema
from app.crud.noti import get_notification_count
from app.utils.get_current_user import get_current_user
from app.models import profile
from app.schemas import user_schema

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

    return templates.TemplateResponse("pages/admin_signup.html",
                                      {'request': request})


@router.post("/")
async def create_admin_post(request: Request,
                            email=Form(...),
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
async def set_teams_profile(request: Request,
                            team_names: list[str] = Form(...),
                            current_user=Depends(get_current_user),
                            ):
    print(team_names)
    # 일반 계정인지 확인
    if isinstance(current_user, user_schema.User):
        return RedirectResponse(url="/signin")

    else:
        teamdata = TeamData()
        teamdata.create_teams(team_names=team_names)

        return RedirectResponse('/admin')
