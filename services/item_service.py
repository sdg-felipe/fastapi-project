from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.item import ItemModel
from schemas.item import ItemCreate
from fastapi import HTTPException

def get_items(db: Session, category: Optional[str], skip: int, limit: int):
    query = db.query(ItemModel)
    if category:
        query = query.filter(ItemModel.category == category)

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "skip": skip
    }

def get_user_items(db: Session, user_id: int):
    items = db.query(ItemModel).filter(ItemModel.owner_id == user_id).all()
    return items

def get_item(db: Session, item_id: int):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

def create_item(db: Session, user_id: int, new_item: ItemCreate):
    try:
        db_new_item = ItemModel(
            name=new_item.name,
            description=new_item.description,
            price_per_day=new_item.price_per_day,
            image_url=new_item.image_url,
            category=new_item.category,
            owner_id=user_id
        )
        db.add(db_new_item)
        db.commit()
        db.refresh(db_new_item)
        return db_new_item
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Something went wrong")

def update_item(db: Session, item_id: int, user_id: int, updated_item: ItemCreate):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Option unavailable")

    for key, value in updated_item.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, item_id: int, user_id: int):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Option unavailable")

    db.delete(item)
    db.commit()