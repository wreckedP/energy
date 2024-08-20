from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, insert
from app.database.crud.base_crud import Session, CRUDBase
from app.database.models.installation import InstallationModel
from app.schemas.installation import InstallationCreateDTO, InstallationUpdateDTO
from app.database.crud.user import user_crud

class CRUDInstallation(
    CRUDBase[InstallationModel, InstallationCreateDTO, InstallationUpdateDTO]
):
    def create(
        self,
        session: Session,
        create_obj: InstallationCreateDTO,
        owner_email: str,
    ) -> InstallationModel:

        installation_data = jsonable_encoder(create_obj)
        installation_data["owner_email"] = owner_email

        # TODO: encrypt api_key

        new_installation = session.scalar(
            insert(self.model).values(installation_data).returning(self.model)
        )

        user = user_crud.get_by_email(session, owner_email)
        user.installaiton_id =  new_installation.id

        session.commit()
        return new_installation

    def get_with_meters(self, session: Session, installaiton_id: int) -> InstallationModel:
        return session.scalars(
            select(self.model)
            .filter(self.model.id == installaiton_id)
            .options(selectinload(self.model.meters))
        )


installation_crud = CRUDInstallation(InstallationModel)
