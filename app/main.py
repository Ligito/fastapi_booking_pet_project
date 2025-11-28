from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .admin.auth import authentication_backend
from .config import settings
from .database import engine

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms

from app.pages.router import router as router_pages
from app.images.router import router as router_images
from app.admin.views import UsersAdmin, BookingsAdmin, UsersHotels, UsersRooms

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from sqladmin import Admin, ModelView

from starlette.middleware.sessions import SessionMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняемый при запуске приложения
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield  # Здесь происходит выполнение приложения
    # Код, выполняемый при завершении приложения
    await redis.close()


app = FastAPI(lifespan=lifespan)




#app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY) # !!! Добавил для настройки аутентификации админки


app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

app.include_router(router_pages)
app.include_router(router_images)


admin = Admin(app, engine, authentication_backend=authentication_backend) # , authentication_backend=authentication_backend
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(UsersHotels)
admin.add_view(UsersRooms)








