import json

import pytest
from fastapi import status
from httpx import AsyncClient
from kafka import KafkaConsumer  # type:ignore[import-untyped]
from tests import factory as data_factory


pytestmark = pytest.mark.anyio


async def test_get_applications(
    client: AsyncClient, factory: data_factory.FactoryCallback
):
    await factory(data_factory.ApplicationFactory, 10)
    response = await client.get("/application/")
    assert response.status_code == status.HTTP_200_OK


async def test_create_application(client: AsyncClient):
    data = {"username": "Alev", "description": "Prosto people"}
    response = await client.post("/application/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

    consumer = KafkaConsumer(
        "topic",
        group_id="my_group",
        value_deserializer=json.loads,
    )
    message = next(consumer).value
    consumer.close()
    assert all(message.get(key) == value for key, value in data.items())
    assert "id" in message
    assert "created_at" in message


@pytest.mark.parametrize(
    "username, status_code",
    [
        ("Alev", status.HTTP_200_OK),
        ("", status.HTTP_200_OK),
        ("Lizadfkjv", status.HTTP_404_NOT_FOUND),
    ],
)
async def test_filter_by_username(
    client: AsyncClient,
    factory: data_factory.FactoryCallback,
    username,
    status_code,
):
    await factory(data_factory.ApplicationFactory, 10)
    if status_code == status.HTTP_200_OK and username != "":
        await factory(data_factory.ApplicationFactory, username=username)

    response = await client.get("/application/", params={"username": username})
    assert response.status_code == status_code
