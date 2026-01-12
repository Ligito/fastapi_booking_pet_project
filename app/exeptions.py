from fastapi import HTTPException, status


class BookingException(HTTPException): # <-- наследуемся от HTTPException,

    status_code = 500 # <-- задаем значения по умолчанию
    detail = ""
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistException(BookingException): # <-- обязательно наследуемся от нашего класса
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"

class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"

class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"

class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"

class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"

class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED

class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"

class ThereIsNotDataToDelete(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Неверно указаны данные для удаления"

class ThereIsNotHotelWithThisID(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Нет отеля с таким id"

class RoomFullyBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Не осталось свободных номеров"

class HotelIncorrectParameters(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверные параметры поиска отеля"

# UserAlreadyExistExceptions = HTTPException(
#     status_code=status.HTTP_409_CONFLICT,
#     detail="Пользователь уже существует",
# )

# IncorrectEmailOrPasswordException = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Неверная почта или пароль",
# )

# TokenExpiredException = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Токен истек",
# )

# TokenAbsentException = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Токен отсутствует",
# )

# IncorrectTokenFormatException = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Неверный формат токена",
# )

# UserIsNotPresentException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)