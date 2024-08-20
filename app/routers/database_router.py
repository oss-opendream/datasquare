import os
from dotenv import load_dotenv
from datetime import timedelta, datetime
from typing import Annotated

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi import Cookie
from jose import jwt
from starlette import status

from app.crud.user_crud import UserData
from app.crud.team_crud import TeamData
from app.schemas import user_schema


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')

@router.get('/databases', name='databases')
async def databases(request: Request):
    return templates.TemplateResponse('pages/success.html', {
        'request': request,
        'company_name': 'Your Company',
        'current_year': datetime.now().year
    })