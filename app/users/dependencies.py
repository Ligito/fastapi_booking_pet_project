from fastapi import Request, Depends
from jose import jwt, JWTError
from datetime import datetime, UTC

from app.config import settings
from app.exeptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, \
    UserIsNotPresentException
from app.users.dao import UsersDAO



def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except IncorrectTokenFormatException:
        # Как позже выяснилось, ключ exp автоматически проверяется
        # командой jwt.decode, поэтому отдельно проверять это не нужно
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user

# async def get_current_user_raw(token: str):
#     print(f"Validating token: {token[:20]}...")
#     print(f"Using SECRET_KEY: {settings.SECRET_KEY[:10]}...")  # ← ← ←
#     print(f"Using ALGORITHM: {settings.ALGORITHM}")  # ← ← ←
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, settings.ALGORITHM
#         )
#         print(f"Decoded payload: {payload}")
#     except jwt.JWTError as e:
#         print(f"JWT decode error: {e}")
#         return None
#
#     expire: str = payload.get("exp")
#     if (not expire) or (int(expire) < datetime.now(UTC).timestamp()):
#         print("Token expired")
#         return None
#
#     user_id: str = payload.get("sub")
#     if not user_id:
#         print("No user_id in token")
#         return None
#
#     user = await UsersDAO.find_by_id(int(user_id))
#     if not user:
#         print(f"User with id {user_id} not found")
#         return None
#
#     print(f"User authenticated: {user.email}")
#     return user

