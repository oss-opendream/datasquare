'''개인 프로필 페이지 관리 라우터 함수'''

import os
import base64
from typing import Annotated
from datetime import timedelta, datetime
from dotenv import load_dotenv

from fastapi import APIRouter, Request, Depends, Form, File, UploadFile
from fastapi.responses import JSONResponse
from jose import jwt

# from app.crud.noti import get_notification_count
from app.crud.team_crud import TeamData
from app.crud.user_crud import UserData
from app.schemas.user_schema import User
from app.utils.get_current_user import get_current_user
from sqlalchemy.exc import IntegrityError
from starlette import status
from app.utils.template import template


profilerouter = APIRouter(prefix="/profile")

load_dotenv(override=True)

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = str(os.getenv('SECRET_KEY'))
ALGORITHM = str(os.getenv('ALGORITHM'))


@profilerouter.get("/")
async def personal(
    request: Request,
    current_user=Depends(get_current_user)
):
    '''개인 프로필 출력 라우터 '''

    personal_db = UserData().get_user(
        current_user.profile_id, key="profile_id")

    team_name = TeamData().get_current_user_team_data(current_user.profile_id)

    return template.TemplateResponse(
        'pages/personal.html',
        {
            'request': request,
            # 'notification_count': get_notification_count(current_user.profile_id),
            'image': base64.b64encode(personal_db.profile_image).decode('utf-8'),
            'name': personal_db.name,
            'email': personal_db.email,
            'phone': personal_db.phone_number,
            'department': team_name.team_name,
        }
    )


@profilerouter.get("/profile_edit")
async def personal_edit(
        request: Request,
        current_user=Depends(get_current_user)
):
    '''개인 프로필 수정 페이지 라우터'''

    return template.TemplateResponse(
        'pages/personal_edit.html',
        {
            'request': request,
            # 'notification_count': get_notification_count(current_user.profile_id),
            'image': base64.b64encode(current_user.profile_image).decode('utf-8'),
            'name': current_user.name,
            'email': current_user.email,
            'phone': current_user.phone_number,
            'department': current_user.department,
        }
    )


@profilerouter.post("/")
async def personal_post(request: Request,
                        name: Annotated[str, Form()],
                        email: Annotated[str, Form()],
                        phone_number: Annotated[str, Form()],
                        image: UploadFile = File(...),
                        current_user=Depends(get_current_user)):
    ''' 수정된 개인 프로필 저장 라우터 '''

    # image가 없을 때 기본값으로 처리
    if image.filename != "":
        image_bytes = await image.read()
    else:
        image_bytes = current_user.profile_image

    update_data = User(
        profile_id=current_user.profile_id,
        name=name,
        email=email,
        phone_number=phone_number,
        profile_image=image_bytes,
        department=current_user.department,
        team_id=current_user.team_id
    )

    try:
        UserData().update_user_data(current_user.profile_id, update_data)

        data = {
            'sub': email,  # 사용자 식별
            'exp': datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_MINUTES)  # token 유효기간
        }
        access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

        response = template.TemplateResponse(
            'pages/personal.html',
            {
                'request': request,
                # 'notification_count': get_notification_count(update_data.profile_id),
                'image': base64.b64encode(update_data.profile_image).decode('utf-8'),
                'name': update_data.name,
                'email': update_data.email,
                'phone': update_data.phone_number,
                'department': current_user.department,
            }
        )
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax'
        )

        return response

    except IntegrityError:
        return JSONResponse(
            content={
                'error': 'This account already exists. Please check your phone number and email again.'
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )


@profilerouter.get('/team')
async def team_profile_get(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    '''team 프로필 View 페이지 라우터'''

    team = TeamData()

    team_data = team.get_current_user_team_data(current_user.profile_id)
    team_members = team.get_team_members(team_data.profile_id)
    team_manager = team_data.team_manager

    return template.TemplateResponse(
        'pages/team_profile_view.html',
        {
            'request': request,
            # 'notification_count': get_notification_count(current_user.profile_id),
            'team': team_data,
            'members': team_members,
            'has_permission': (team_manager == current_user.profile_id)
        }
    )


@profilerouter.post('/team')
async def team_profile_post(
    origin_name: str = Form(...),
    team_name: str = Form(...),
    team_intro: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    '''team 프로필 View 페이지 저장 라우터'''

    team = TeamData()
    try:
        team.modify_team_info_profile(origin_name, team_name, team_intro)

        ret = JSONResponse(
            content={
                "status": "success",
            }
        )
    except:
        ret = JSONResponse(
            content={
                "error": 'The team name must be unique. Please check the team name.'
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return ret
