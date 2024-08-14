from fastapi import FastAPI

from api.api_travels import api_router
from api.api_users import api_router_user
from database import create_tables
from web.web_travels import web_router


def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
app.include_router(web_router)
app.include_router(api_router_user)
