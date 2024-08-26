from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.utils.org import get_org_metadata
from app.schemas.org import DBConnectionForm
from app.crud.org import DBInterface
from app.database import get_db
from app.utils.template import template


router = APIRouter(prefix='/admin/org')


@router.get('/')
async def main(request: Request):
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
    db: Session = Depends(get_db)
):
    form_data = DBConnectionForm(
        host=host,
        port=port,
        db_name=db_name,
        user=user,
        password=password,
    )

    org_metadata = get_org_metadata(form_data)
    if not org_metadata:
        return RedirectResponse('/404')  # Temporary solution

    db_interface = DBInterface(db, org_metadata)
    if not db_interface.create_metadata():
        return RedirectResponse('/404')  # Temporary solution

    return RedirectResponse('/database')
