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
    password: str = Form(...),
    db: Session = Depends(get_db),
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

    db_interface = DBInterface(db, org_metadata)
    if not db_interface.create_metadata():
        raise HTTPException(
            status_code=404,
            detail='Failed to create metadata for the organization using the provided database connection.'
        )

    return RedirectResponse('/database')
