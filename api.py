from fastapi import FastAPI
from routers import auth, item, rental, user

def register_routes(app: FastAPI):
    app.include_router(auth.router)
    app.include_router(item.router)
    app.include_router(rental.router)
    app.include_router(user.router)