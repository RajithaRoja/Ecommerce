from models import Rating
from typing import Annotated
from .auth import get_db, get_current_user
from fastapi import HTTPException, Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status


router = APIRouter(
    prefix='',
    tags=['Rating']
)


class CreateRating(BaseModel):
    Menu_id: int
    product_name: str
    feedback: str
    rating: int


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/rating", status_code=status.HTTP_201_CREATED)
async def rating(
        user: user_dependency,
        create: CreateRating,
        db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    address_model = Rating(**create.dict(), owner_id=user.get('user_id'))
    db.add(address_model)
    db.commit()
    return {"Message": "Rating stored successfully"}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_ratings(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Rating).all()

