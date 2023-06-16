from typing import Annotated
from .address import user_dependency
from passlib.context import CryptContext
from models import Payment
from fastapi import HTTPException, Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_db


router = APIRouter(
    prefix='/payment',
    tags=['payment']
)


db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class payment(BaseModel):
    payment_method:  str
    number_of_product: int
    Amount: int
    status: str


# Payment
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_payment_status(db: db_dependency,
                       user: user_dependency,
                       Payments: payment):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    create_model = Payment(**Payments.dict(), owner_id=user.get('user_id'))

    db.add(create_model)
    db.commit()
    return {"Message": "Status Created Successfully"}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_payment_status(user: user_dependency, db: Session = Depends(get_db)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    users = db.query(Payment).all()
    return users

