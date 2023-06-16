from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from .address import user_dependency
from sqlalchemy.orm import Session
from starlette import status
from models import Orders
from .register import db_dependency, get_db


router = APIRouter(prefix='/Order',
                   tags=['Order'])


class CreateOrder(BaseModel):
    menu_id: int
    menu_name: str
    number_of_items: int
    Quantity: int
    order_status: str


# Orders
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(db: db_dependency,
                       user: user_dependency,
                       create_order: CreateOrder):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    create_model = Orders(**create_order.dict(), owner_id=user.get('user_id'))

    db.add(create_model)
    db.commit()
    return {"Message": "Order placed Successfully"}


class UpdateOrder(BaseModel):
    order_status: str


@router.put("/delivered/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_order_delivery_status(user: user_dependency,
                                       order_id: int,
                                       db: db_dependency, update_order: UpdateOrder):
    # Retrieve the order from the database
    if user is None or user.get('role') != 'driver':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    order = db.query(Orders).filter(Orders.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Update the delivery status
    order.order_status = update_order.order_status
    db.commit()

    return {"Message": 'Order updated successfully'}


@router.delete("/by_id", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user: user_dependency, db: db_dependency, delete_id: int):
    if user is None or user.get('role') != 'user':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    delete_model = db.query(Orders).filter(Orders.order_id == delete_id)\
        .filter(Orders.owner_id == user.get('user_id')).first()
    if delete_model is None:
        raise HTTPException(status_code=404, detail='Not found.')
    db.query(Orders).filter(Orders.order_id == delete_id)\
        .filter(Orders.owner_id == user.get('user_id')).delete()
    db.commit()
    return {"Message": "Deleted Successfully"}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_orders(
        user: user_dependency,
        page: int = 1,  # Page number (default: 1)
        db: Session = Depends(get_db)
):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')

    limit = 3  # Number of users per page
    offset = (page - 1) * limit  # Calculate the offset based on the current page

    users = db.query(Orders).offset(offset).limit(limit + 1).all()

    # Check if there are more users beyond the current page
    has_next = len(users) > limit
    users = users[:limit]  # Trim the users list to the requested limit

    response_data = {
        'users': users,
        'page': page,
        'has_next': has_next
    }

    if has_next:
        next_page = page + 1
        response_data['next_page'] = next_page

    return response_data