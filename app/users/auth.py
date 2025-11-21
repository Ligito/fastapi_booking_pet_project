from datetime import datetime, UTC

from asyncpg.pgproto.pgproto import timedelta
from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from app.users.dao import UsersDAO
from app.config import settings


pwd_context = CryptContext(schemes=['bcrypt'])

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(hours=1)
    to_encode.update({"exp": expire.timestamp()})
    encode_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )

    return encode_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Версия bcrypt -"bcrypt==3.2.2" или bcrypt==4.0.1, т.к. на данный момент новая версия bcrypt==5.0.0 не совместима с passlib==1.7.4
# Поэтому пришлось занизить версию либо использовать прямой bcrypt (без passlib)

# import bcrypt
#
# def get_password_hash(password: str) -> str:
#     # bcrypt автоматически генерирует соль
#     hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     return hashed.decode('utf-8')
#
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return bcrypt.checkpw(
#         plain_password.encode('utf-8'),
#         hashed_password.encode('utf-8')
#     )