from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from typing import List


def create_animal(db: Session, animal: schemas.AnimalCreate):
    db_animal = models.Animal(
        name=animal.name,
        species=animal.species,
        age=animal.age,
        is_native=animal.is_native  
    )
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    
    if animal.guider_ids:
        guiders = db.query(models.Guider).filter(models.Guider.id.in_(animal.guider_ids)).all()
        db_animal.guiders = guiders
        db.commit()
        
    return db_animal

def get_animal(db: Session, animal_id: int):
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal

def get_animals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Animal).offset(skip).limit(limit).all()

def update_animal(db: Session, animal_id: int, animal: schemas.AnimalCreate):
    db_animal = get_animal(db, animal_id)
    
    db_animal.name = animal.name
    db_animal.species = animal.species
    db_animal.age = animal.age
    
    if animal.guider_ids:
        guiders = db.query(models.Guider).filter(models.Guider.id.in_(animal.guider_ids)).all()
        db_animal.guiders = guiders
    
    db.commit()
    db.refresh(db_animal)
    return db_animal

def delete_animal(db: Session, animal_id: int):
    db_animal = get_animal(db, animal_id)
    db.delete(db_animal)
    db.commit()
    return {"message": "Animal deleted successfully"}


def create_guider(db: Session, guider: schemas.GuiderCreate):
    db_guider = models.Guider(
        name=guider.name,
        age=guider.age,
        service_hours=guider.service_hours,
        gender=guider.gender 
    )
    db.add(db_guider)
    db.commit()
    db.refresh(db_guider)
    return db_guider

def get_guider(db: Session, guider_id: int):
    guider = db.query(models.Guider).filter(models.Guider.id == guider_id).first()
    if not guider:
        raise HTTPException(status_code=404, detail="Guider not found")
    return guider

def get_guiders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Guider).offset(skip).limit(limit).all()

def update_guider(db: Session, guider_id: int, guider: schemas.GuiderCreate):
    db_guider = get_guider(db, guider_id)
    
    db_guider.name = guider.name
    db_guider.age = guider.age
    db_guider.service_hours = guider.service_hours
    
    db.commit()
    db.refresh(db_guider)
    return db_guider

def delete_guider(db: Session, guider_id: int):
    db_guider = get_guider(db, guider_id)
    db.delete(db_guider)
    db.commit()
    return {"message": "Guider deleted successfully"}


def create_guest(db: Session, guest: schemas.GuestCreate):
    db_guest = models.Guest(
        name=guest.name,
        visit_date=guest.visit_date,
        is_adult=guest.is_adult 
    )
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    
    if guest.guider_ids:
        guiders = db.query(models.Guider).filter(models.Guider.id.in_(guest.guider_ids)).all()
        db_guest.guiders = guiders
        db.commit()
        
    return db_guest

def get_guest(db: Session, guest_id: int):
    guest = db.query(models.Guest).filter(models.Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest

def get_guests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Guest).offset(skip).limit(limit).all()

def update_guest(db: Session, guest_id: int, guest: schemas.GuestCreate):
    db_guest = get_guest(db, guest_id)
    
    db_guest.name = guest.name
    db_guest.visit_date = guest.visit_date
    
    if guest.guider_ids:
        guiders = db.query(models.Guider).filter(models.Guider.id.in_(guest.guider_ids)).all()
        db_guest.guiders = guiders
    
    db.commit()
    db.refresh(db_guest)
    return db_guest

def delete_guest(db: Session, guest_id: int):
    db_guest = get_guest(db, guest_id)
    db.delete(db_guest)
    db.commit()
    return {"message": "Guest deleted successfully"}

def assign_guider_to_animal(db: Session, animal_id: int, guider_id: int):
    animal = get_animal(db, animal_id)
    guider = get_guider(db, guider_id)
    
    animal.guiders.append(guider)
    db.commit()
    return animal

def remove_guider_from_animal(db: Session, animal_id: int, guider_id: int):
    animal = get_animal(db, animal_id)
    guider = get_guider(db, guider_id)
    
    animal.guiders.remove(guider)
    db.commit()
    return animal

def assign_guider_to_guest(db: Session, guest_id: int, guider_id: int):
    guest = get_guest(db, guest_id)
    guider = get_guider(db, guider_id)
    
    guest.guiders.append(guider)
    db.commit()
    return guest

def remove_guider_from_guest(db: Session, guest_id: int, guider_id: int):
    guest = get_guest(db, guest_id)
    guider = get_guider(db, guider_id)
    
    guest.guiders.remove(guider)
    db.commit()
    return guest