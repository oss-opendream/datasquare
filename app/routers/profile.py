'''개인 프로필 페이지 관리 라우터 함수'''

import base64
from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from app.crud.noti import get_notification_count
from app.crud.team_crud import TeamData
from app.crud.user_crud import UserData
from app.schemas.user_schema import User
from app.utils.get_current_user import get_current_user


templates = Jinja2Templates(directory='app/templates')
profilerouter = APIRouter(prefix="/profile")


@profilerouter.get("/")
async def personal(
    request: Request,
    current_user=Depends(get_current_user)
):
    '''개인 프로필 출력 라우터 '''

    personal_db = UserData().get_user(
        current_user.profile_id, key="profile_id")

    team_name = TeamData().get_current_user_team_data(current_user.profile_id)

    return templates.TemplateResponse(
        'pages/personal.html',
        {
            'request': request,
            'notification_count': get_notification_count(current_user.profile_id),
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


@profilerouter.get('/team')
async def team_profile_get(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    '''team 프로필 View 페이지 라우터'''

    team = TeamData()

    team_data = team.get_current_user_team_data(current_user.profile_id)
    team_members = team.get_team_members(team_data.profile_id)

    return templates.TemplateResponse(
        'pages/team_profile_view.html',
        {
            'request': request,
            'notification_count': get_notification_count(current_user.profile_id),
            'team': team_data,
            'members': team_members,
            'has_permission': True
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
    team.modify_team_info_profile(origin_name, team_name, team_intro)

    ret = JSONResponse(
        content={
            "status": "success",
        }
    )

    return ret
