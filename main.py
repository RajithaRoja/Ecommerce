from fastapi import FastAPI
import models
from database import engine
from routers import auth, register, address, menu, orders, rating, payment, DeliverStatus

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(register.router)
app.include_router(orders.router)
app.include_router(address.router)
app.include_router(menu.router)
app.include_router(rating.router)
app.include_router(payment.router)
app.include_router(DeliverStatus.router)

