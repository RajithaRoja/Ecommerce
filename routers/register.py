from typing_extensions import Annotated
from .address import user_dependency
from passlib.context import CryptContext
from models import User
from fastapi import HTTPException, Depends, APIRouter
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_db


router = APIRouter(
    prefix='/user',
    tags=['user']
)


db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUser(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    password: str
    role: str


# New User Registration
@router.post("/user", status_code=status.HTTP_201_CREATED)
def user_register(create_new: CreateUser, db: db_dependency):
    existing_user = db.query(User).filter(
        (User.email == create_new.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='A user with the provided email already exists'
        )

    create_user_model = User(
        username=create_new.name,
        email=create_new.email,
        phone_number=create_new.phone_number,
        hashed_password=bcrypt_context.hash(create_new.password),
        role=create_new.role
    )

    db.add(create_user_model)
    db.commit()

    return {"message": "Registered successfully"}


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(User).all()

