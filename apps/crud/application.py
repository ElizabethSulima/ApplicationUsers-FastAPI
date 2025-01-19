from typing import Sequence

import sqlalchemy as sa
from crud.common import Base
from models.application import Application


class ApplicationCrud(Base):
    def __init__(self, session):
        super().__init__(session)
        self.model = Application

    async def get_user_name(self, username: str) -> Sequence[Application]:
        applications = await self.session.scalars(
            sa.select(self.model).where(self.model.username == username)
        )
        return applications.all()
