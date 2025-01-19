from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Application(BaseModel):
    username: str
    description: str


class ApplicationCreate(Application):
    pass


class ApplicationResponse(Application):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
