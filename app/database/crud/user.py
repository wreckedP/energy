from typing import Any, Dict
from fastapi.encoders import jsonable_encoder

from sqlalchemy import select, insert

from app.settings.security import create_hash, verify_hash
from app.database.models.user import UserModel
from app.schemas.user import UserCreateDTO, UserPublic
from app.database.crud.base_crud import Session, CRUDBase  # ,log



class CRUDUser(CRUDBase[UserModel, UserCreateDTO, UserPublic]):
    def create(self, session: Session, create_obj: UserCreateDTO) -> UserModel:
        user_data = jsonable_encoder(create_obj)
        del user_data["password"]
        user_data["hashed_password"] = create_hash(create_obj.password)

        return session.scalar(
            insert(self.model).values(user_data).returning(self.model)
        )

    def get_by_email(self, session: Session, email: str) -> UserModel:
        return session.scalars(
            select(self.model).where(self.model.email == email)
        ).first()


    def authenticate(self, session: Session, email: str, password: str) -> UserModel | None:
        user = self.get_by_email(session, email=email)

        if user and user.hashed_password and not verify_hash(password, user.hashed_password):
            return None
        return user

    def update_self(
        self,
        session: Session,
        model: UserModel,
        update_obj: Dict[str, Any],
    ) -> UserModel:
        if "password" in update_obj.keys():
            hashed_password = create_hash(update_obj["password"])
            del update_obj["password"]
            update_obj["hashed_password"] = hashed_password

        updated_user = self.put(session, database_model=model, update_obj=update_obj)

        return updated_user


user_crud = CRUDUser(UserModel)
