from pydantic import BaseModel
from datetime import datetime

class RentalBase(BaseModel):
    item_id: int
    tenant_id: int
    owner_id: int
    start_date: datetime
    end_date: datetime
    status: str = "pending"

class RentalCreate(RentalBase):
    pass

class Rental(RentalBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True