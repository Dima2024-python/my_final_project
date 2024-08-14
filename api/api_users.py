import uuid

from fastapi import HTTPException, APIRouter, Request
from starlette import status
import dao


from pydantic import BaseModel, Field, EmailStr

from utils.send_email import create_welcome_letter, send_email

api_router_user = APIRouter(prefix='/api/users', tags=['User'])


class NewUser(BaseModel):
    name: str = Field(max_length=50, min_length=1, examples=["Victor"], description='Name of the new user')
    email: EmailStr = Field(examples=['travel_agency2024@ukr.net'], description='Email of the user')
    password: str = Field(description="Your password", examples=['12345678'], min_length=8)


@api_router_user.post("/verify/", status_code=status.HTTP_201_CREATED)
def create_user(request: Request, new_user: NewUser) -> NewUser:
    print(request.__dict__)
    maybe_user = dao.get_user_by_email(new_user.email)
    if maybe_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')

    created_user = dao.create_user(**new_user.dict())
    email_body = create_welcome_letter({
        'name': created_user.name,
        'link': f'{request.base_url}api/users/verify/{created_user.user_uuid}'
    })
    send_email([created_user.email], mail_body=email_body, mail_subject='Verification')
    return created_user


@api_router_user.get("/verify/{user_uuid}")
def verify_user(user_uuid: uuid.UUID):
    maybe_user = dao.get_user_by_uuid(user_uuid)
    if not maybe_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Wrong data')
    dao.activate_account(maybe_user)
    return {'Verified': True, 'user': maybe_user.email}
