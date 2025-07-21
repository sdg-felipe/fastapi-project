from fastapi import FastAPI

from api import register_routes
from db.db import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

register_routes(app)
