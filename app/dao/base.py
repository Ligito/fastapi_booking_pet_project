from app.database import async_session_maker
from sqlalchemy import select, insert, delete


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

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

