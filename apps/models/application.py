from datetime import datetime

from models.base import Base, int_pk
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int_pk]
    username: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()  # pylint:disable=E1102
    )
