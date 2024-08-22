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
async def personal(request: Request, current_user=Depends(get_current_user)):

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


@router.get("/profile_edit")
async def personal_edit(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(
        'pages/personal_edit.html',
        {
            'request': request,
            'notification_count': get_notification_count(current_user.profile_id),
            'image': base64.b64encode(current_user.profile_image).decode('utf-8'),
            'name': current_user.name,
            'email': current_user.email,
            'phone': current_user.phone_number,
            'department': current_user.department,
        }
    )


@router.post("/")
async def personal_post(request: Request,
                        name: Annotated[str, Form()],
                        email: Annotated[str, Form()],
                        phone_number: Annotated[str, Form()],
                        image: UploadFile = File(...),
                        current_user=Depends(get_current_user)):

    # image가 없을 때
    if image.filename != "":
        image_bytes = await image.read()
    else:
        image_bytes = current_user.profile_image

    update_data = user_schema.User(
        profile_id=current_user.profile_id,
        name=name,
        email=email,
        phone_number=phone_number,
        profile_image=image_bytes,
        department=current_user.department,
        team_id=current_user.team_id
    )

    UserData().update_user_data(current_user.profile_id, update_data)

    return templates.TemplateResponse(
        'pages/personal.html',
        {
            'request': request,
            'notification_count': get_notification_count(update_data.profile_id),
            'image': base64.b64encode(update_data.profile_image).decode('utf-8'),
            'name': update_data.name,
            'email': update_data.email,
            'phone': update_data.phone_number,
            'department': current_user.department,
        }
    )
