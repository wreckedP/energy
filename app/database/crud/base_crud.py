from typing import Any, Dict, Generic, Type, TypeVar

from fastapi.exceptions import HTTPException
from pydantic import BaseModel as DTO
from sqlalchemy import select

from sqlalchemy.orm import Session
from app.core.logger import log  # create cutstom crud logger

from app.database.models.base_model import BaseModel

DatabaseModel = TypeVar("DatabaseModel", bound=BaseModel)
CreateDTO = TypeVar("CreateDTO", bound=DTO)
UpdateDTO = TypeVar("UpdateDTO", bound=DTO)


class CRUDBase(Generic[DatabaseModel, CreateDTO, UpdateDTO]):
    def __init__(self, model: Type[DatabaseModel]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, session: Session, id: int) -> DatabaseModel | None:

        result = session.scalars(select(self.model).filter_by(id=id)).one_or_none()
        return result

    def get_multi(
        self,
        session: Session,
        skip: int | None = 0,
        limit: int | None = 100,
    ) -> list[DatabaseModel]:

        database_models = session.scalars(
            select(self.model).offset(skip).limit(limit)
        ).all()
        if not database_models:
            raise HTTPException(404, "None found")

        return database_models

    def put(
        self,
        session: Session,
        database_model: DatabaseModel,
        update_obj: Dict[str, Any],
    ) -> DatabaseModel:
        primary_keys = database_model.primary_keys()

        for field, value in update_obj.items():
            if field not in primary_keys:
                setattr(database_model, field, value)
        try:
            session.commit()
        except Exception as err:
            print(f"update error: {err}")
            session.rollback()

        return database_model
