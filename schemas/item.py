from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str
    price_per_day: int
    image_url: str
    category: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True