from fastapi import APIRouter,HTTPException
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from models import Users
from typing import Annotated, Optional
from database import SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status
from datetime import datetime, timedelta, timezone
from jose.exceptions import JWTError
SECRET_KEY ="40b3d9678976e1df1ef1b77479b010136adef45d34e14d0776da9a7be5cc0f43"
ALGORITHM = "HS256"
router = APIRouter(  prefix='/auth',

  tags=['auth'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
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

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #ペイロードの中の sub キーに対応する値（この場合はユーザー名）を取り出します。if username is None or user_id is None:id キーに対応する値（この場合はユーザーID）を取り出します。
     username: str = payload.get("sub")
     user_id: int = payload.get("id")
     if username is None or user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="ユーザーを検証できません")
     return {"username": username, "id": user_id}
    except JWTError:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="ユーザーを検証できません")



@router.post("/", status_code=status.HTTP_201_CREATED)

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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)  
    token = create_access_token(user.username, user.id, timedelta(minutes=15))

    return {'access_token': token, 'token_type': 'bearer'}






