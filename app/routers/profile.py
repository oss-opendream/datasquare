import os
import base64
from dotenv import load_dotenv
from datetime import timedelta, datetime
from typing import Annotated

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, Depends, Form, HTTPException, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi import Cookie, Response
from jose import jwt
from starlette import status

from app.crud.user_crud import UserData
from app.crud.team_crud import TeamData
from app.schemas import user_schema
from app.crud.noti import get_notification_count
from app.routers.sign import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')
router = APIRouter(prefix="/profile")


@router.get("/")
def proflie(request: Request, current_user: user_schema.User = Depends(get_current_user)):

    return templates.TemplateResponse(
        'pages/profile.html',
        {
            'request': request,
            'notification_count': get_notification_count(current_user.profile_id)
        }
    )


@router.get("/personal")
def personal(request: Request, current_user: user_schema.User = Depends(get_current_user)):

    personal_db = UserData().get_user(
        current_user.profile_id, key="profile_id")

    team_name = TeamData().get_current_user_team_name(current_user.profile_id)

    return templates.TemplateResponse(
        'pages/personal.html',
        {
            'request': request,
            'notification_count': get_notification_count(current_user.profile_id),
            'image': base64.b64encode(personal_db.profile_image).decode('utf-8'),
            'name': personal_db.name,
            'email': personal_db.email,
            'phone': personal_db.phone_number,
            'department': team_name,
        }
    )
