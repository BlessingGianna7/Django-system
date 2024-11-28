from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .database import Base


animal_guider = Table(
    'animal_guider',
    Base.metadata,
    Column('animal_id', Integer, ForeignKey('animals.id', ondelete='CASCADE')),
    Column('guider_id', Integer, ForeignKey('guiders.id', ondelete='CASCADE'))
)

guest_guider = Table(
    'guest_guider',
    Base.metadata,
    Column('guest_id', Integer, ForeignKey('guests.id', ondelete='CASCADE')),
    Column('guider_id', Integer, ForeignKey('guiders.id', ondelete='CASCADE'))
)

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    is_native = Column(Boolean, nullable=False)  
    
    guiders = relationship("Guider", 
                          secondary=animal_guider,
                          back_populates="animals")

class Guider(Base):
    __tablename__ = "guiders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    service_hours = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)  
    
    animals = relationship("Animal", 
                          secondary=animal_guider,
                          back_populates="guiders")
    guests = relationship("Guest", 
                         secondary=guest_guider,
                         back_populates="guiders")

class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    visit_date = Column(String, nullable=False)
    is_adult = Column(Boolean, nullable=False)
    
    guiders = relationship("Guider", 
                          secondary=guest_guider,
                          back_populates="guests")