from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from app.config import settings
from app.exeptions import (
    IncorrectEmailOrPasswordException,
    IncorrectTokenFormatException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.users.auth import authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(email, password)
        if user:
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    # В типизации ответа кода необходимо ставить bool или Optional[bool] а не Optional[RedirectResponse] (как в курсе),
    # так не работает потому что GET /admin/ → authenticate() возвращает RedirectResponse → ОШИБКА NotImplementedError
    async def authenticate(self, request: Request) -> Optional[bool]:
        token = request.session.get("token")

        if not token:
            return False

        try:
            user = await get_current_user(token)
            if not user:
                return False
            return True

        except (TokenExpiredException, IncorrectTokenFormatException, UserIsNotPresentException):
            request.session.clear()
            return False




authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)


















# class AdminAuth(AuthenticationBackend):
#     async def login(self, request: Request) -> bool:
#         form = await request.form()
#         email, password = form["username"], form["password"]
#
#         user = await authenticate_user(email, password)
#         if not user:
#             return False
#
#         access_token = create_access_token({"sub": str(user.id)})
#         request.session.update({"token": access_token})
#         return True
#
#     async def logout(self, request: Request) -> bool:
#         # Usually you'd want to just clear the session
#         request.session.clear()
#         return True
#
#     async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
#         token = request.session.get("token")
#
#         if not token:
#             return RedirectResponse(request.url_for("admin:login"), status_code=302)
#
#         user = await get_current_user(token)
#         if not user:
#             return RedirectResponse(request.url_for("admin:login"), status_code=302)
#
#
# authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
