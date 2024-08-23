'''사용자 로그인과 회원가입 기능을 하는 Router.'''

import os
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

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = str(os.getenv('SECRET_KEY'))
ALGORITHM = str(os.getenv('ALGORITHM'))


@router.get('/signin', response_class=HTMLResponse, name='auth.signin')
async def singin_get(request: Request):
    return templates.TemplateResponse(request=request,
                                      name='pages/sign_in.html',
                                      )


@router.post('/signin/post',
             response_class=HTMLResponse,
             response_model=user_schema.Token,
             name='sign_post'
             )
async def signin_post(request: Request,
                      form_data: OAuth2PasswordRequestForm = Depends(),):

    # check user and password

    userdata_obj = UserData()
    user = userdata_obj.get_user_password(form_data.username, key='email')
    url = '/feed'

    # admin 계정일 때는 Page를 다르게 보이게 함.
    if not user:
        user = userdata_obj.get_admin_data(form_data.username)
        url = '/admin/init'

    if not user or not userdata_obj.pwd_context.verify(form_data.password, user.password):
        return RedirectResponse(url='/signin?error=비밀번호가 일치하지 않습니다.', status_code=status.HTTP_302_FOUND)

    data = {
        'sub': user.email,  # 사용자 식별
        'exp': datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_MINUTES)  # token 유효기간
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    # HTTPOnly 쿠키로 토큰 반환
    response = RedirectResponse(
        url=url, status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key='access_token', value=access_token, httponly=True, secure=False, samesite='Lax'
    )

    return response


@router.get('/signup', name='auth.signup')
async def signup_get(request: Request):

    departments = TeamData().get_team_name()

    return templates.TemplateResponse('pages/sign_up.html',
                                      context={'request': request,
                                               'departments': departments}
                                      )


@router.post('/signup')
async def signup_post(
    request: Request,
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    password2: Annotated[str, Form()],
    phone_number: Annotated[str, Form()],
    department: Annotated[str, Form()],
    image: UploadFile = File(...)
):

    image_content = await image.read()

    try:
        user_create = user_schema.UserCreate(
            name=name,
            email=email,
            password=password,
            password2=password2,
            phone_number=phone_number,
            department=department,
            image=image_content
        )
    except:
        return JSONResponse(content={"error": "이메일형식이 올바르지않습니다. 다시 작성해주세요"}, status_code=status.HTTP_400_BAD_REQUEST)
    userdata_obj = UserData()

    # 비번확인
    if password != password2:
        return JSONResponse(content={"error": "비밀번호가 일치하지 않습니다."}, status_code=status.HTTP_400_BAD_REQUEST)
    # admin 계정에 email이 존재한다면 회원가입 못하도록 함
    if userdata_obj.get_admin_data(user_create.email):
        return JSONResponse(content={"error": "admin계정에 존재하는 계정입니다. 다른 계정으로 회원가입해주세요"}, status_code=status.HTTP_400_BAD_REQUEST)

    if userdata_obj.get_user_password(email, key='email'):  # 이미 회원가입이 되어있는지 확인
        return JSONResponse(content={"error": "이미 존재하는 계정입니다. 다른 계정으로 회원가입해주세요"}, status_code=status.HTTP_400_BAD_REQUEST)
    else:
        userdata_obj.create_user(user_create=user_create)

        return RedirectResponse(url='/signin', status_code=status.HTTP_302_FOUND)


@router.get('/logout', response_class=HTMLResponse)
def logout(response: Response):

    response = RedirectResponse(url='/signin')
    response.delete_cookie("access_token")

    return response
