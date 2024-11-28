from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import analytics, crud, schemas, models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Wildlife Conservation API"}

@app.post("/animals/", response_model=schemas.Animal)
def create_animal_view(data: schemas.AnimalCreate, db: Session = Depends(get_db)):
    return crud.create_animal(db=db, animal=data)

@app.get("/animals/{animal_id}", response_model=schemas.Animal)
def read_animal_view(animal_id: int, db: Session = Depends(get_db)):
    return crud.get_animal(db=db, animal_id=animal_id)

@app.put("/animals/{animal_id}", response_model=schemas.Animal)
def update_animal_view(animal_id: int, data: schemas.AnimalUpdate, db: Session = Depends(get_db)):
    return crud.update_animal(db=db, animal_id=animal_id, animal=data)

@app.delete("/animals/{animal_id}")
def delete_animal_view(animal_id: int, db: Session = Depends(get_db)):
    return crud.delete_animal(db=db, animal_id=animal_id)

@app.get("/animals/", response_model=List[schemas.Animal])
def list_animals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_animals(db=db, skip=skip, limit=limit)


@app.post("/guiders/", response_model=schemas.Guider)
def create_guider_view(data: schemas.GuiderCreate, db: Session = Depends(get_db)):
    return crud.create_guider(db=db, guider=data)

@app.get("/guiders/{guider_id}", response_model=schemas.Guider)
def read_guider_view(guider_id: int, db: Session = Depends(get_db)):
    return crud.get_guider(db=db, guider_id=guider_id)

@app.put("/guiders/{guider_id}", response_model=schemas.Guider)
def update_guider_view(guider_id: int, data: schemas.GuiderUpdate, db: Session = Depends(get_db)):
   return crud.update_guider(db=db, guider_id=guider_id, guider=data)  

@app.get("/analytics")  
async def get_analytics(db: Session = Depends(get_db)):
    try:
        analytics_instance = analytics.WildlifeAnalytics(db)
        return {
            'basic_stats': analytics_instance.get_basic_stats(),
            'animal_distribution': analytics_instance.get_animal_distribution(),
            'guest_analysis': analytics_instance.get_guest_analysis(),
            'guider_analysis': analytics_instance.get_guider_analysis(),
            'complex_analysis': analytics_instance.get_complex_analysis()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/{analysis_type}")  
async def get_specific_analytics(
    analysis_type: str,
    db: Session = Depends(get_db)
):
    try:
        analytics_instance = analytics.WildlifeAnalytics(db)
        
        analysis_types = {
            "basic": analytics_instance.get_basic_stats,
            "animals": analytics_instance.get_animal_distribution,
            "guests": analytics_instance.get_guest_analysis,
            "guiders": analytics_instance.get_guider_analysis,
            "complex": analytics_instance.get_complex_analysis
        }
        
        if analysis_type not in analysis_types:
            raise HTTPException(
                status_code=404, 
                detail=f"Analysis type not found. Available types: {list(analysis_types.keys())}"
            )
        
        return analysis_types[analysis_type]()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))