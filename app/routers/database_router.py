from datetime import datetime

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.schemas.user_schema import User
from app.utils.get_current_user import get_current_user
from app.crud.noti import get_notification_count

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/databases', name='databases')
async def databases(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse('pages/success.html', {
        'request': request,
        'company_name': 'Your Company',
        'current_year': datetime.now().year,
        'notification_count': get_notification_count(current_user.profile_id)
    })
