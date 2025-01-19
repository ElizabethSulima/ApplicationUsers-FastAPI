import fastapi as fa
from core.dependency import AsyncSessionDepency
from core.producer import producer
from crud.application import ApplicationCrud
from fastapi_pagination import Page, paginate
from models.application import Application
from schemas import application as sha


app_router = fa.APIRouter(prefix="/application", tags=["applications"])


@app_router.get("/", response_model=Page[sha.ApplicationResponse])
async def get_applications(
    session: AsyncSessionDepency, username: str | None = None
):
    application_crud = ApplicationCrud(session)

    if username is not None and username != "":
        applications = await application_crud.get_user_name(username)

        if len(applications) == 0:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_404_NOT_FOUND,
                detail="User name not found",
            )
        return paginate(applications)

    return paginate(await application_crud.get_items())


@app_router.post("/", response_class=fa.responses.JSONResponse)
async def create_application(
    session: AsyncSessionDepency, data: sha.ApplicationCreate
):
    application: Application = await ApplicationCrud(session).create_item(
        data.model_dump()
    )
    await session.commit()
    await session.refresh(application)

    message = {
        "id": application.id,
        "username": application.username,
        "description": application.description,
        "created_at": application.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
    producer.send("topic", message)
    producer.flush()
    return fa.responses.JSONResponse(
        content="Application success created",
        status_code=fa.status.HTTP_201_CREATED,
    )
