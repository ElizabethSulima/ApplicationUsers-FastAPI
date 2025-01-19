from typing import Any, Sequence

import sqlalchemy as sa
from models.base import MODEL, TypeModel
from sqlalchemy.ext.asyncio import AsyncSession


class Base:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.model: TypeModel

    async def create_item(self, data: dict[str, Any]) -> MODEL:
        item = await self.session.scalar(
            sa.insert(self.model).returning(self.model).values(**data)
        )
        return item  # type: ignore[return-value]

    async def get_items(self) -> Sequence[MODEL]:
        result = await self.session.scalars(
            sa.select(self.model).order_by(self.model.id.desc())
        )
        return result.all()
