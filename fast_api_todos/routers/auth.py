from fastapi import APIRouter
from pydantic import BaseModel

from models import Users

router = APIRouter()
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

# パスワードのハッシュ化に使用するbcryptの設定
# bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# ユーザー作成リクエスト用のPydanticモデル
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/create_user/")
async def create_user(create_user_request: CreateUserRequest):
    # ユーザーモデルを作成
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        role=create_user_request.role,
    )
    return create_user_model


