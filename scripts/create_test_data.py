from app.database import SessionLocal
from app.models import Animal, Guider, Guest
from datetime import datetime, timedelta
import random

def create_test_data():
    db = SessionLocal()
    try:
      
        db.query(Animal).delete()
        db.query(Guider).delete()
        db.query(Guest).delete()
        db.commit()

        guiders = [
            Guider(
                name=f"Guider {i}",
                age=random.randint(25, 55),
                gender=random.choice(['M', 'F']),
                service_hours=random.randint(100, 1000)
            ) for i in range(1, 6)  
        ]
        db.add_all(guiders)
        db.commit()

        animals = [
            Animal(
                name=f"Animal {i}",
                species=random.choice(['Lion', 'Elephant', 'Giraffe', 'Zebra', 'Rhino']),
                age=random.randint(1, 15),
                is_native=random.choice([True, False])
            ) for i in range(1, 11)  
        ]
        db.add_all(animals)
        db.commit()

      
        guests = [
            Guest(
                name=f"Guest {i}",
                visit_date=datetime.now() - timedelta(days=random.randint(0, 365)),
                is_adult=random.choice([True, False])
            ) for i in range(1, 21)  
        ]
        db.add_all(guests)
        db.commit()

   
        for animal in animals:
            animal.guiders = random.sample(guiders, random.randint(1, 3))

        for guest in guests:
            guest.guiders = random.sample(guiders, random.randint(1, 2))

        db.commit()
        print("Test data created successfully!")

    except Exception as e:
        print(f"Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()