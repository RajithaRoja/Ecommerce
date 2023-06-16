from models import Address, Orders
from typing import Annotated
from .auth import get_db, get_current_user
from fastapi import HTTPException, Depends, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status


router = APIRouter(
    prefix='',
    tags=['address']
)


class CreateAddress(BaseModel):
    state: str = Field(min_length=1)
    city: str = Field(min_length=1)
    street: str
    pincode: int


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Address).filter(Address.owner_id == user.get('user_id')).all()


@router.get("/read_by_id", status_code=status.HTTP_200_OK)
async def read_by_id(user: user_dependency, db: db_dependency, Address_id: int):
    if user is None or user.get('role') != 'driver':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    toto_model = db.query(Address).filter(Address.address_id == Address_id).first()
    if toto_model is not None:
        return toto_model
    raise HTTPException(status_code=404, detail='Not Found')


@router.post("/address", status_code=status.HTTP_201_CREATED)
async def create_address(
        user: user_dependency,
        create: CreateAddress,
        db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    address_model = Address(**create.dict(), owner_id=user.get('user_id'))
    db.add(address_model)
    db.commit()
    return {"Message": "Address stored successfully"}


@router.put("/update_address", status_code=status.HTTP_204_NO_CONTENT)
async def update_address(user: user_dependency, db: db_dependency,
                         update_address: CreateAddress,
                         Address_id: int):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    update_model = db.query(Address).filter(Address.address_id == Address_id).first()
    if update_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    update_model.state = update_address.state
    update_model.city = update_address.city
    update_model.street = update_address.street
    update_model.pincode = update_address.pincode

    db.add(update_model)
    db.commit()
    return {"message": "Updated successfully"}


@router.delete("/by_id", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user: user_dependency, db: db_dependency, delete_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    delete_model = db.query(Address).filter(Address.address_id == delete_id)\
        .filter(Address.owner_id == user.get('user_id')).first()
    if delete_model is None:
        raise HTTPException(status_code=404, detail='Not found.')
    db.query(Address).filter(Address.address_id == delete_id)\
        .filter(Address.owner_id == user.get('user_id')).delete()
    db.commit()
    return {"message": "Deleted successfully"}



