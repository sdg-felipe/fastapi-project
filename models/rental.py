from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from db.db import Base

class RentalModel(Base):
    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    tenant_id = Column(Integer, ForeignKey("users.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String(50))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)