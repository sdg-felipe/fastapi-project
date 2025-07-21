from typing import List, Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from dependencies.auth import user_dependency
from dependencies.db import db_dependency
from models.item import ItemModel
from schemas.item import Item, ItemCreate
from services import item_service

router = APIRouter(
    prefix="/item",
    tags=["item"],
)

# GET ALL ITEMS
@router.get("/")
async def get_items(db: db_dependency,
                    category: Optional[str] = None,
                    skip: int = 0,
                    limit: int = 100):
    return item_service.get_items(db, category, skip, limit)

# USER ITEMS
@router.get("/me", response_model=List[Item])
async def get_user_items(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Could not get user")
    return item_service.get_user_items(db, user.get("id"))

# GET ITEM BY ID
@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int, db: db_dependency):
    return item_service.get_item(db, item_id)

#  CREATE ITEM
@router.post("/", response_model=Item, status_code=201)
async def create_item(user: user_dependency, new_item: ItemCreate, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Could not get user")
    return item_service.create_item(db, user.get("id"), new_item)

# UPDATE ITEM
@router.put("/{id}", response_model=Item)
async def update_item(
        item_id: int,
        updated_item: ItemCreate,
        user: user_dependency,
        db: db_dependency
):
    return item_service.update_item(db, item_id, user.get("id"), updated_item)

# DELETE ITEM
@router.delete("/{id}", status_code=204)
async def delete_item(item_id: int, user: user_dependency, db: db_dependency):
    item_service.delete_item(db, item_id, user.get("id"))
