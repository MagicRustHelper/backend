from typing import Generic, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import BaseDeclarative

ModelType = TypeVar('ModelType', bound=BaseDeclarative)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(self, session: AsyncSession, id: int) -> Optional[ModelType]:
        return await session.get(self.model, id)

    async def get_multi(self, session: AsyncSession, *, offset: int = 0, limit: int = 100) -> list[ModelType]:
        statement = select(self.model).offset(offset).limit(limit)
        return await session.scalars(statement)

    async def create(self, session: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_dict = obj_in.dict(exclude_none=True)
        db_obj = self.model(**obj_in_dict)  # type: ignore
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, session: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = jsonable_encoder(obj_in)
        update_data = obj_in.dict(exclude_none=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, *, id: int) -> ModelType:
        obj = await self.get(session, id)
        await session.delete(obj)
        await session.commit()
        return obj
