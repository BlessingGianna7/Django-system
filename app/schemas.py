from typing import List, Optional
from pydantic import BaseModel


class GuiderBase(BaseModel):
    name: str
    age: int
    service_hours: int
    gender: str

class GuiderCreate(GuiderBase):
    pass

class GuiderUpdate(GuiderBase):
    name: Optional[str] = None
    age: Optional[int] = None
    service_hours: Optional[int] = None

class Guider(GuiderBase):
    id: int

    class Config:
        from_attributes = True

class AnimalBase(BaseModel):
    name: str
    species: str
    age: int
    is_native: bool 

class AnimalCreate(AnimalBase):
    guider_ids: List[int] = []
    
class AnimalUpdate(AnimalBase):
    name: Optional[str] = None
    species: Optional[str] = None
    age: Optional[int] = None
    guider_ids: Optional[List[int]] = []

class Animal(AnimalBase):
    id: int
    guiders: Optional[List[Guider]] = []
    
    class Config:
        from_attributes = True

class GuestBase(BaseModel):
    name: str
    visit_date: str
    is_adult: bool 

class GuestCreate(GuestBase):
    guider_ids: List[int] = []

class GuestUpdate(GuestBase):
    name: Optional[str] = None
    visit_date: Optional[str] = None
    guider_ids: Optional[List[int]] = []

class Guest(GuestBase):
    id: int
    guiders: Optional[List[Guider]] = []

    class Config:
        from_attributes = True