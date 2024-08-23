from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    password2: str
    phone_number: str
    department: str
    image: bytes


class User(BaseModel):
    profile_id: int
    name: str
    email: EmailStr
    phone_number: str
    profile_image: bytes
    department: str
    team_id: int


class AdminUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str  # token 종류는 Bearer로 고정하여 사용
    username: str  # 사용자 Email
