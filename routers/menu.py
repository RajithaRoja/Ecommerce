from sqlalchemy.orm import Session
from .register import db_dependency, get_db
from .address import user_dependency
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from starlette import status
from models import Menus

router = APIRouter(
    prefix='/menu',
    tags=['menu']
)


class Menu(BaseModel):
    item_name: str
    price: int
    quantity: int


@router.post("/menu", status_code=status.HTTP_201_CREATED)
async def create_menu(user: user_dependency, db: db_dependency, Create_Menu: Menu):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    create_menu = Menus(
        item_name=Create_Menu.item_name,
        price=Create_Menu.price,
        quantity=Create_Menu.quantity
    )
    db.add(create_menu)
    db.commit()
    return {"Message": 'Product Added Successfully'}


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_menu(request: Request, page: int = 1, limit: int = 5, db: Session = Depends(get_db)):
    total_users = db.query(Menus).count()
    offset = (page - 1) * limit
    users = db.query(Menus).offset(offset).limit(limit).all()

    # Calculate the number of pages
    total_pages = (total_users // limit) + (1 if total_users % limit > 0 else 0)

    response_data = {
        'page': page,
        'limit': limit,
        'total_users': total_users,
        'total_pages': total_pages,
        'users': users
    }

    return response_data


@router.get("/read_by_id", status_code=status.HTTP_200_OK)
async def read_by_id(db: db_dependency, Address_id: int):
    toto_model = db.query(Menus).filter(Menus.menu_id == Address_id).first()
    if toto_model is not None:
        return toto_model
    raise HTTPException(status_code=404, detail='Not Found')


@router.put("/update_menu", status_code=status.HTTP_204_NO_CONTENT)
async def update_menu(user: user_dependency, db: db_dependency,
                         update_menu: Menu,
                         menu_id: int):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    update_model = db.query(Menus).filter(Menus.menu_id == menu_id).first()
    if update_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    update_model.item_name = update_menu.item_name
    update_model.price = update_menu.price
    update_model.quantity = update_menu.quantity

    db.add(update_model)
    db.commit()
    return {"message": "Updated successfully"}


@router.delete("/delete_menu}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu(user: user_dependency, db: db_dependency, menu_id: int):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Menus).filter(Menus.menu_id == menu_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Menu not found. ')
    db.query(Menus).filter(Menus.menu_id == menu_id).delete()
    db.commit()