from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException

from dependencies.auth import user_dependency
from dependencies.db import db_dependency
from models.rental import RentalModel
from schemas.rental import Rental, RentalCreate
from services import rental_service

router = APIRouter(
    prefix="/rental",
    tags=["rental"]
)

def is_item_available(
        item_id: int,
        start_rental: datetime,
        end_rental: datetime,
        db: db_dependency
):
    overlapping = db.query(RentalModel).filter(
        RentalModel.item_id == item_id,
        RentalModel.status.in_(["approved", "pending"]),
        RentalModel.end_date >= start_rental,
        RentalModel.start_date <= end_rental
    ).first()
    return overlapping is None


# GET USER RENTALS
@router.get("/me", response_model=List[Rental])
async def get_user_rentals(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return rental_service.get_user_rentals(db, user.get("id"))

# GET RECEIVED RENTALS
@router.get("/received", response_model=List[Rental])
async def get_received_rentals(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return rental_service.get_received_rentals(db, user.get("id"))

# GET UNAVAILABLE ITEM DATES
@router.get("/unavailable/{item_id}")
async def get_unavailable_dates(
        item_id: int,
        db: db_dependency
):
    return {"unavailable": rental_service.get_unavailable_dates(db, item_id)}

# GET USER RENTAL BY ID
@router.get("/{rental_id}", response_model=Rental)
async def get_rental_by_id(rental_id: int, tenant_id: int, user:user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return rental_service.get_rental_by_id(db, rental_id, tenant_id, user.get("id"))

#  CREATE RENTAL
@router.post("/", status_code=201, response_model=Rental)
async def create_rental(new_rental: RentalCreate, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Could not get user")
    return rental_service.create_rental(db, user.get("id"), new_rental)

# UPDATE RENTAL STATUS
@router.put("/{rental_id}/status", response_model=Rental)
async def update_rental_status(
        rental_id: int,
        status: str,
        user: user_dependency,
        db: db_dependency
):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return rental_service.update_rental_status(db, rental_id, status, user.get("id"))