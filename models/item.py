from sqlalchemy import Column, Integer, String, ForeignKey

from db.db import Base

class ItemModel(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(500), index=True)
    price_per_day = Column(Integer)
    image_url = Column(String(255), index=True)
    category = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))