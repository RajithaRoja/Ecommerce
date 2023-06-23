from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
import uvicorn
from database import engine
from routers import auth, register, address, menu, orders, rating, payment, DeliverStatus

app = FastAPI()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(register.router)
app.include_router(orders.router)
app.include_router(address.router)
app.include_router(menu.router)
app.include_router(rating.router)
app.include_router(payment.router)
app.include_router(DeliverStatus.router)

