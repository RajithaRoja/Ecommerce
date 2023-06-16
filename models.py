from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(String)
    hashed_password = Column(String)
    role = Column(String)


class Address(Base):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True, index=True)
    state = Column(String)
    city = Column(String)
    street = Column(String)
    pincode = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.user_id"))


class Menus(Base):
    __tablename__ = 'menus'

    menu_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)


class Rating(Base):
    __tablename__ = 'rating'

    rating_id = Column(Integer, primary_key=True, index=True)
    Menu_id = Column(Integer)
    product_name = Column(String)
    rating = Column(Integer)
    feedback = Column(String)
    owner_id = Column(Integer, ForeignKey("users.user_id"))


class Orders(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer)
    menu_name = Column(String)
    number_of_items = Column(Integer)
    Quantity = Column(Integer)
    order_status = Column(String)
    owner_id = Column(Integer, ForeignKey("users.user_id"))


class deliver(Base):
    __tablename__ = 'status'

    deliver_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    number_of_orders = Column(Integer)
    cost = Column(Integer)
    amount_status = Column(String)
    order_status = Column(String)
    owner_id = Column(Integer, ForeignKey("users.user_id"))


class Payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(Integer, primary_key=True, index=True)
    payment_method = Column(String)
    number_of_product = Column(Integer)
    Amount = Column(Integer)
    status = Column(String)
    owner_id = Column(Integer, ForeignKey("users.user_id"))

