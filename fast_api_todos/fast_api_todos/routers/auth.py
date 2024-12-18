from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from models import Users
from typing import Annotated, Optional
from database import SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status
from datetime import datetime, timedelta, timezone
SECRET_KEY ="40b3d9678976e1df1ef1b77479b010136adef45d34e14d0776da9a7be5cc0f43"
ALGORITHM = "HS256"
router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
db_dependency = Annotated[Session, Depends(get_db)]

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

# パスワードのハッシュ化に使用するbcryptの設定
# bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ユーザー作成リクエスト用のPydanticモデル
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
class Token(BaseModel):
  access_token: str
  token_type: str


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
      return False

    if not bcrypt_context.verify(password, user.hashed_password):
      return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username,'id':user_id}
    expires=datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)



@router.post("/auth", status_code=status.HTTP_201_CREATED)

async def create_user(db: db_dependency,create_user_request: CreateUserRequest):

    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),  # ⚠️要修正
        is_active=True

    )
    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed Authentication'  
    token = create_access_token(user.username, user.id, timedelta(minutes=15))

    return {'access_token': token, 'token_type': 'bearer'}





