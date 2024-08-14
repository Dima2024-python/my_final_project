from fastapi import FastAPI

from api.api_travels import api_router
from database import create_tables


def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(api_router)


@app.get("/")
def index() -> dict:
    return {"status": "200"}
