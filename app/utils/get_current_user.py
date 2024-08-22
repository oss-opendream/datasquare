import os
from dotenv import load_dotenv

from fastapi import HTTPException, Request
from jose import jwt

from app.crud.user_crud import UserData


load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = eval(
    str(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')


def get_current_user(request: Request):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail='Not authenticated')

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get('sub')

        if user_id is None:
            raise HTTPException(
                status_code=401, detail='Invalid authentication credentials')

        user_obj = UserData()

        # admin 계정일때의 처리
        user = user_obj.get_admin_data(user_id)

        if not user:
            user = UserData().get_user(user_id, key='email')

        if user is None:
            raise HTTPException(status_code=401, detail='User not found')

        return user

    except jwt.JWTError:
        raise HTTPException(
            status_code=401, detail='Invalid authentication credentials')
