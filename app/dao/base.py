from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(id=model_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = f"Database Exc: Cannot find data by id = {model_id}"
            elif isinstance(e, Exception):
                msg = f"Unknown Exc: Cannot find data by id = {model_id}"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            filter_str = ', '.join(f"{k}={v!r}" for k, v in filter_by.items())
            if isinstance(e, SQLAlchemyError):
                msg = f"Database Exc: Cannot find data with filter: {filter_str}"
            else:
                msg = f"Unknown Exc: Cannot find data with filter: {filter_str}"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**data)
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def delete_object(cls, **filter_by):
        async with async_session_maker() as session:
            # Находим объекты которые будем удалять
            find_query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(find_query)
            objects_to_delete = result.scalars().all()

            if objects_to_delete:
                # Удаляем объекты
                delete_query = delete(cls.model).filter_by(**filter_by)
                await session.execute(delete_query)
                await session.commit()

            # Возвращаем список удаленных объектов
            return objects_to_delete

