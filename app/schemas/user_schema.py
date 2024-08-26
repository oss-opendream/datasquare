'''user 정보 및 인증 관련 schema를 정의하는 class'''


from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    '''sign up 시 유효성 검사를 위한 schema class'''

    name: str
    email: EmailStr
    password: str
    password2: str
    phone_number: str
    department: str
    image: bytes


class User(BaseModel):
    '''user 데이터 유효성 검사를 위한 schema class'''

    profile_id: int
    name: str
    email: EmailStr
    phone_number: str
    profile_image: bytes
    department: str
    team_id: int


class AdminUser(BaseModel):
    '''admin 계정 데이터 유효성 검사를 위한 schema class'''

    id: int
    name: str
    email: EmailStr
    password: str


class Token(BaseModel):
    '''인증 토큰 데이터 유효성 검사를 위한 schema class'''

    access_token: str
    token_type: str  # token 종류는 Bearer로 고정하여 사용
    username: str  # 사용자 Email
