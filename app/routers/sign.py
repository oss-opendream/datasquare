'''사용자 로그인과 회원가입 기능을 하는 Router.'''

import os
from dotenv import load_dotenv
from datetime import timedelta, datetime
from typing import Annotated

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from starlette import status

from app.crud.user_crud import UserData
from app.crud.team_crud import TeamData
from app.schemas import user_schema


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = eval(str(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')


@router.get('/signin', response_class=HTMLResponse)
async def singin_get(request: Request):
    return templates.TemplateResponse(request=request,
                                      name='sign_in.html',
                                      )

@router.post('/signin', response_class=HTMLResponse, response_model=user_schema.Token)
async def signin_post(request: Request,
                      form_data: OAuth2PasswordRequestForm = Depends(),):

    # check user and password
    userdata_obj = UserData()
    user = userdata_obj.get_user(form_data.username)
    
    if not user or not userdata_obj.pwd_context.verify(form_data.password, user.password):

        return RedirectResponse(url='/signin?error=비밀번호가 일치하지 않습니다.'
                                , status_code=status.HTTP_302_FOUND)

    data = {
        "sub": user.profile_id, # 사용자 식별 
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # token 유효기간
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return templates.TemplateResponse("success.html", 
                                      {"request": request}
                                    )


@router.get("/signup")
async def signup_get(request: Request):
    
    departments = TeamData().get_team_name()

    return templates.TemplateResponse('sign_up.html',
                                      context={'request': request
                                               , "departments": departments}
                                    )


@router.post("/signup")
async def signup_post(request: Request
                        , name: Annotated[str, Form()]
                        , email: Annotated[str, Form()]
                        , password: Annotated[str, Form()]
                        , password2: Annotated[str, Form()]
                        , phone_number: Annotated[str, Form()]
                        , department: Annotated[str, Form()]
                      ):

    try:
        user_create = user_schema.UserCreate(
            name=name,
            email=email,
            password=password,
            password2=password2,
            phone_number=phone_number,
            department=department
        )
    except:
        return RedirectResponse(url='/signup?error=Email 형식이 유효하지 않습니다.', status_code=status.HTTP_302_FOUND)

    # 이미 회원가입이 되어있는지 확인
    userdata_obj = UserData()

    if userdata_obj.get_user(email = user_create.email):
        return RedirectResponse(url='/signup?error=이미 등록된 계정입니다. 로그인해주세요', status_code=status.HTTP_302_FOUND)
    else:
        userdata_obj.create_user( user_create=user_create)

        return templates.TemplateResponse('success.html',
                                          context={'request': request})

