'''데이터베이스 페이지 관리 라우터 모듈'''

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette import status

from app.utils.org import get_org_metadata
from app.schemas.org import DBConnectionForm
from app.crud.org import DBInterface
from app.database import get_db
from app.utils.template import template
from app.schemas import user_schema
from app.utils.get_current_user import get_current_user
from app.schemas.user_schema import User

router = APIRouter(prefix='/admin/org')


@router.get('/')
async def main(request: Request, current_user=Depends(get_current_user)):

    if not isinstance(current_user, user_schema.AdminUser):
        raise HTTPException(status_code=401)

    return template.TemplateResponse(
        'pages/org.html',
        {'request': request}
    )


@router.post('/')
async def handle_insertion_request(
    host: str = Form(...),
    port: int = Form(...),
    db_name: str = Form(...),
    user: str = Form(...),
    password: Optional[str] = Form(None),
    current_user=Depends(get_current_user)
):
    if not isinstance(current_user, user_schema.AdminUser):
        raise HTTPException(status_code=401)

    form_data = DBConnectionForm(
        host=host,
        port=port,
        db_name=db_name,
        user=user,
        password=password,
    )

    org_metadata = get_org_metadata(form_data)
    if not org_metadata:
        raise HTTPException(
            status_code=404,
            detail='Organization metadata not found for the provided database connection details.'
        )
    db_interface = DBInterface()
    if not db_interface.create_metadata(org_metadata):
        raise HTTPException(
            status_code=404,
            detail='Failed to create metadata for the organization using the provided database connection.'
        )

    return RedirectResponse('/admin/org/databases', status_code=303)


@router.get('/databases', name='databases')
async def databases(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    '''데이터베이스 페이지 함수'''
    databases = DBInterface().read_databases()

    return template.TemplateResponse('pages/databases.html', {
        'request': request,
        'databases': databases
        # 'company_name': 'Your Company',
        # 'current_year': datetime.now().year,
        # 'notification_count': get_notification_count(current_user.profile_id)
    })
