from fastapi import APIRouter, Form, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

import dao
from utils.jwt_auth import get_user_web, set_cookies_web

templates = Jinja2Templates(directory="templates")

web_router = APIRouter(
    prefix="",
)


@web_router.get('/')
def index(request: Request):
    context = {
        'request': request,
        'travels': dao.get_all_travel(20, 0),
        "title": "Main page"}
    return templates.TemplateResponse("index.html", context=context)


@web_router.get('/search')
def search(request: Request):
    context = {
        'request': request,
        'travels': dao.get_all_travel(20, 0),
        'search': True,
        "title": 'Search'}
    return templates.TemplateResponse("index.html", context=context)


@web_router.get("/search_by_country", include_in_schema=True)
@web_router.post("/search_by_country", include_in_schema=True)
def search_by_country(request: Request, query: str = Form(None)):
    context = {
        "request": request,
        'search': True,
        "travels": dao.get_travel_by_country(query),
        "title": "Main page",
    }
    response = templates.TemplateResponse("index.html", context=context)
    return response


@web_router.get("/search_by_price", include_in_schema=True)
@web_router.post("/search_by_price", include_in_schema=True)
def search_by_price(request: Request, query: float = Form(None)):
    context = {
        "request": request,
        'search': True,
        "travels": dao.get_travel_by_price(query),
        "title": "Main page",
    }
    response = templates.TemplateResponse("index.html", context=context)
    return response


@web_router.get("/search_by_hotel_class", include_in_schema=True)
@web_router.post("/search_by_hotel_class", include_in_schema=True)
def search_by_hotel_class(request: Request, query: int = Form(None)):
    print(query, 888888888888888888888888)
    context = {
        "request": request,
        'search': True,
        "travels": dao.get_travel_by_hotel_class(query),
        "title": "Main page",
    }
    response = templates.TemplateResponse("index.html", context=context)
    return response




