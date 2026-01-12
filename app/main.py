import time
from contextlib import asynccontextmanager

from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView
from starlette.middleware.sessions import SessionMiddleware
from fastapi_versioning import VersionedFastAPI

from app.admin.views import BookingsAdmin, UsersAdmin, UsersHotels, UsersRooms
from app.bookings.router import router as router_bookings
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users
from app.logger import logger

from .admin.auth import authentication_backend
from .config import settings
from .database import engine


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


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

app.include_router(router_pages)
app.include_router(router_images)

# app = VersionedFastAPI(app,
#     version_format='{major}',
#     prefix_format='/v{major}',
#     # description='Greet users with a nice message',
#     # middleware=[
#     #     Middleware(SessionMiddleware, secret_key='mysecretkey')
#     # ]
# )

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(UsersHotels)
admin.add_view(UsersRooms)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process_Time"] = str(process_time)
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response

app.mount("/static", StaticFiles(directory="app/static"), "static")






