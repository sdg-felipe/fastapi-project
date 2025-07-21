from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.rental import RentalModel
from schemas.rental import RentalCreate

def is_item_available(
    item_id: int,
    start_rental: datetime,
    end_rental: datetime,
    db: Session
):
    overlapping = db.query(RentalModel).filter(
        RentalModel.item_id == item_id,
        RentalModel.status.in_(["approved", "pending"]),
        RentalModel.end_date >= start_rental,
        RentalModel.start_date <= end_rental
    ).first()
    return overlapping is None

def get_user_rentals(db: Session, user_id: int):
    return db.query(RentalModel).filter(RentalModel.tenant_id == user_id).all()

def get_received_rentals(db: Session, user_id: int):
    return db.query(RentalModel).filter(RentalModel.owner_id == user_id).all()

def get_unavailable_dates(db: Session, item_id: int):
    rentals = db.query(RentalModel).filter(
        RentalModel.item_id == item_id,
        RentalModel.status.in_(["approved", "pending"]),
    ).all()

    return [
        {"start": rental.start_date.date().isoformat(), "end": rental.end_date.date().isoformat()}
        for rental in rentals
    ]

def get_rental_by_id(db: Session, rental_id: int, tenant_id: int, user_id: int):
    if user_id != tenant_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    rental = db.query(RentalModel).filter(RentalModel.id == rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental

def create_rental(db: Session, user_id: int, new_rental: RentalCreate):
    if not is_item_available(new_rental.item_id, new_rental.start_date, new_rental.end_date, db):
        raise HTTPException(status_code=400, detail="Item not available")
    try:
        db_new_rental = RentalModel(
            item_id=new_rental.item_id,
            tenant_id=user_id,
            owner_id=new_rental.owner_id,
            start_date=new_rental.start_date,
            end_date=new_rental.end_date,
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(db_new_rental)
        db.commit()
        db.refresh(db_new_rental)
        return db_new_rental
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Something went wrong")

def update_rental_status(
    db: Session,
    rental_id: int,
    status: str,
    user_id: int
):
    rental = db.query(RentalModel).filter(RentalModel.id == rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    if rental.owner_id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    rental.status = status
    rental.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(rental)
    return rental
