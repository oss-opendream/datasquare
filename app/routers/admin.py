'''관리자 페이지 관리 라우터 모듈'''


from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from starlette import status

from app.crud.team_crud import TeamData
from app.crud.user_crud import UserData
from app.schemas import user_schema
from app.utils.get_current_user import get_current_user


router = APIRouter(prefix='/admin')
templates = Jinja2Templates(directory='app/templates')


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''앱이 띄워지기 전 실행하는 함수'''

    admin = UserData()

    if not admin.is_admin_table():
        app.redirect_flag = True
        app.setting_tema = False  # 첫 요청에 리다이렉션 플래그 설정
    else:
        app.redirect_flag = False

    yield


@router.get('')
async def redirect_admin(current_user=Depends(get_current_user)):
    '''관리자 식별 후 팀 페이지 함수'''

    if isinstance(current_user, user_schema.AdminUser):
        return RedirectResponse(url='/admin/teams', status_code=status.HTTP_302_FOUND)

    else:
        raise HTTPException(status_code=401)


@router.get('/account/create')
async def create_admin(request: Request):
    '''관리자 관리자 회원가입 페이지 함수'''

    if not UserData().is_admin_table():
        return templates.TemplateResponse(
            'pages/admin_signup.html',
            {
                'request': request
            }
        )
    else:
        raise HTTPException(status_code=401)


@router.post('/account/create')
async def create_admin_post(email=Form(...),
                            name=Form(...),
                            password=Form(...),
                            ):
    '''관리자 로그인 페이지 함수'''

    UserData().create_admin_re(email=email,
                               name=name,
                               password=password)

    return RedirectResponse(
        url='/signin',
        status_code=status.HTTP_302_FOUND
    )


@router.get('/teams/set')
async def teams_settings(
    request: Request,
    current_user=Depends(get_current_user),
):
    '''팀 생성 페이지 함수'''

    if isinstance(current_user, user_schema.AdminUser):
        return templates.TemplateResponse(
            'pages/team_create.html',
            {
                'request': request
            }
        )

    else:
        raise HTTPException(status_code=401)


@router.post('/teams/set')
async def set_teams(
    team_names: list[str] = Form(...),
    current_user=Depends(get_current_user),
):
    '''팀 설정 함수'''

    if isinstance(current_user, user_schema.AdminUser):
        teamdata = TeamData()
        teamdata.create_teams(team_names=team_names)

        return RedirectResponse(
            url='/admin/teams',
            status_code=status.HTTP_302_FOUND,
        )

    else:
        raise HTTPException(status_code=401)


@router.get('/teams', name='team_settings')
async def manage_teams_info(
    request: Request,
    current_user=Depends(get_current_user),
):
    '''팀 관리 페이지 함수'''

    if isinstance(current_user, user_schema.AdminUser):
        team_data = TeamData()
        team_profiles = team_data.get_all()

        if not team_profiles:
            return RedirectResponse(
                url="/admin/teams/set",
                status_code=status.HTTP_302_FOUND,
            )

        return templates.TemplateResponse(
            'pages/team_manage.html',
            {
                'request': request,
                'teams': team_profiles,
            },
        )


@router.post('/teams/update')
async def update_team_info(
    team_names: List[str] = Form(...),
    profile_ids: List[Optional[str]] = Form(...),
    team_managers: List[Optional[str]] = Form(...),
    delete_flags: List[str] = Form(...),
    current_user=Depends(get_current_user),
):
    '''팀 정보 생성, 수정, 삭제 함수'''

    if isinstance(current_user, user_schema.AdminUser):
        team_data = TeamData()
        team_data.modify_team_info(
            profile_ids=profile_ids,
            team_names=team_names,
            team_managers=team_managers,
            delete_flags=delete_flags,
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No permission'
        )

    return RedirectResponse(
        url='/admin/teams',
        status_code=status.HTTP_302_FOUND)
