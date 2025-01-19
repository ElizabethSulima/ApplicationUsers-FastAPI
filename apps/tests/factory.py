from typing import Any, Awaitable, Callable, ParamSpec, Sequence, Type, TypeVar

import sqlalchemy as sa
from faker import Faker
from models.application import Application
from models.base import MODEL, TypeModel
from sqlalchemy.ext.asyncio import AsyncSession


fake = Faker()


class DataFactory:
    def __init__(self, session: AsyncSession) -> None:
        self.list_data: list[dict[str, Any]] = []
        self.model: TypeModel
        self.session = session
        self.response: Any

    # pylint: disable=W0613
    async def generate_data(self, count: int = 1, **kwargs): ...

    # pylint: disable=C0301
    async def write_to_db(self):
        if len(self.list_data) > 1:
            self.response = await self.session.scalars(
                sa.insert(self.model)
                .returning(self.model)
                .values(self.list_data)
            )
        else:
            self.response = await self.session.scalar(
                sa.insert(self.model)
                .returning(self.model)
                .values(self.list_data)
            )

    async def commit(self) -> MODEL | Sequence[MODEL]:
        await self.session.commit()
        if len(self.list_data) == 1:
            await self.session.refresh(self.response)
            return self.response
        return self.response.unique().all()


class ApplicationFactory(DataFactory):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.model = Application

    async def generate_data(self, count=1, **kwargs) -> None:
        self.list_data.extend(
            {
                "username": kwargs.get("username", fake.name()),
                "description": kwargs.get("description", fake.text()),
            }
            for _ in range(count)
        )
        await self.write_to_db()


P = ParamSpec("P")
FACTORY = TypeVar("FACTORY", bound=DataFactory)


TypeFactory = Type[FACTORY]
FactoryCallback = Callable[P, Awaitable[MODEL | Sequence[MODEL]]]
