from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .address import user_dependency
from sqlalchemy.orm import Session
from starlette import status
from .orders import UpdateOrder
from models import deliver
from .register import db_dependency, get_db


router = APIRouter(prefix='/DeliverStatus',
                   tags=['DeliverStatus'])


class CreateStatus(BaseModel):
    user_id: int
    number_of_orders: int
    cost: int
    amount_status: int
    order_status: str


# Orders
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_deliver_status(db: db_dependency,
                       user: user_dependency,
                       create_status: CreateStatus):
    if user is None or user.get('role') != 'driver':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    create_model = deliver(**create_status.dict(), owner_id=user.get('user_id'))

    db.add(create_model)
    db.commit()
    return {"Message": "Status Created Successfully"}


@router.put("/{delivered_by_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_order_delivery_status(user: user_dependency,
                                       order_id: int,
                                       db: db_dependency, update_order: UpdateOrder):
    # Retrieve the order from the database
    if user is None or user.get('role') != 'driver':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    delivery = db.query(deliver).filter(deliver.deliver_id == order_id).first()
    if not delivery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Update the delivery status
    delivery.order_status = update_order.order_status
    db.commit()

    return {"Message": 'Order Delivered successfully'}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_status(user: user_dependency, db: Session = Depends(get_db)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    users = db.query(deliver).all()
    return users