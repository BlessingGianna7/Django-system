import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Dict, Any, List
from . import models

class WildlifeAnalytics:
    def __init__(self, db: Session):
        self.db = db
        self.animals_df = self._get_animals_df()
        self.guests_df = self._get_guests_df()
        self.guiders_df = self._get_guiders_df()

    def _get_animals_df(self) -> pd.DataFrame:
        try:
            animals_query = self.db.query(models.Animal).all()
            if not animals_query:
                return pd.DataFrame(columns=['id', 'name', 'species', 'age', 'is_native', 'guider_ids'])
            
            return pd.DataFrame([{
                'id': animal.id,
                'name': animal.name,
                'species': animal.species,
                'age': animal.age,
                'is_native': animal.is_native,
                'guider_ids': [g.id for g in animal.guiders]
            } for animal in animals_query])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting animals data: {str(e)}")

    def _get_guests_df(self) -> pd.DataFrame:
        try:
            guests_query = self.db.query(models.Guest).all()
            if not guests_query:
                return pd.DataFrame(columns=['id', 'name', 'visit_date', 'is_adult', 'guider_ids'])
            
            return pd.DataFrame([{
                'id': guest.id,
                'name': guest.name,
                'visit_date': guest.visit_date,
                'is_adult': guest.is_adult,
                'guider_ids': [g.id for g in guest.guiders]
            } for guest in guests_query])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting guests data: {str(e)}")

    def _get_guiders_df(self) -> pd.DataFrame:
        try:
            guiders_query = self.db.query(models.Guider).all()
            if not guiders_query:
                return pd.DataFrame(columns=['id', 'name', 'age', 'gender', 'service_hours'])
            
            return pd.DataFrame([{
                'id': guider.id,
                'name': guider.name,
                'age': guider.age,
                'gender': guider.gender,
                'service_hours': guider.service_hours
            } for guider in guiders_query])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting guiders data: {str(e)}")

    def get_basic_stats(self) -> Dict[str, Any]:
        try:
            if self.animals_df.empty or self.guiders_df.empty:
                return {
                    'animals_stats': {},
                    'guiders_stats': {},
                    'total_animals': 0,
                    'total_guests': 0,
                    'total_guiders': 0
                }
            
            return {
                'animals_stats': self.animals_df['age'].describe().to_dict() if not self.animals_df.empty else {},
                'guiders_stats': self.guiders_df['service_hours'].describe().to_dict() if not self.guiders_df.empty else {},
                'total_animals': len(self.animals_df),
                'total_guests': len(self.guests_df),
                'total_guiders': len(self.guiders_df)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calculating basic stats: {str(e)}")

    def get_animal_distribution(self) -> Dict[str, Any]:
        try:
            if self.animals_df.empty:
                return {
                    'native_vs_imported': {},
                    'species_distribution': {}
                }
            
            return {
                'native_vs_imported': self.animals_df['is_native'].value_counts().to_dict(),
                'species_distribution': self.animals_df['species'].value_counts().to_dict()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error analyzing animal distribution: {str(e)}")

    def get_guest_analysis(self) -> Dict[str, Any]:
        try:
            if self.guests_df.empty:
                return {
                    'adult_child_ratio': {},
                    'visits_by_month': {}
                }
            
            return {
                'adult_child_ratio': self.guests_df['is_adult'].value_counts(normalize=True).to_dict(),
                'visits_by_month': pd.to_datetime(self.guests_df['visit_date']).dt.month.value_counts().sort_index().to_dict()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error analyzing guest data: {str(e)}")

    def get_guider_analysis(self) -> Dict[str, Any]:
        try:
            if self.guiders_df.empty:
                return {
                    'gender_distribution': {},
                    'avg_service_hours_by_gender': {}
                }
            
            return {
                'gender_distribution': self.guiders_df['gender'].value_counts().to_dict(),
                'avg_service_hours_by_gender': self.guiders_df.groupby('gender')['service_hours'].mean().to_dict()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error analyzing guider data: {str(e)}")

    def get_complex_analysis(self) -> Dict[str, Any]:
        try:
            if self.animals_df.empty or self.guests_df.empty or self.guiders_df.empty:
                return {
                    'guider_workload': {
                        'animals_per_guider': {},
                        'guests_per_guider': {}
                    },
                    'guest_animal_interactions': {
                        'native_animals_adult_guests': 0,
                        'native_animals_child_guests': 0
                    },
                    'guider_performance': {
                        'avg_animals_by_gender': {},
                        'avg_guests_by_gender': {}
                    }
                }

            animal_guider = self.animals_df.explode('guider_ids')
            guest_guider = self.guests_df.explode('guider_ids')
            
            animal_full = animal_guider.merge(
                self.guiders_df,
                left_on='guider_ids',
                right_on='id',
                suffixes=('_animal', '_guider')
            )
            
            guest_full = guest_guider.merge(
                self.guiders_df,
                left_on='guider_ids',
                right_on='id',
                suffixes=('_guest', '_guider')
            )
            
            return {
                'guider_workload': {
                    'animals_per_guider': animal_guider['guider_ids'].value_counts().describe().to_dict(),
                    'guests_per_guider': guest_guider['guider_ids'].value_counts().describe().to_dict()
                },
                'guest_animal_interactions': {
                    'native_animals_adult_guests': len(animal_full[animal_full['is_native'] & guest_full['is_adult']]),
                    'native_animals_child_guests': len(animal_full[animal_full['is_native'] & ~guest_full['is_adult']])
                },
                'guider_performance': {
                    'avg_animals_by_gender': animal_full.groupby('gender')['id_animal'].nunique().to_dict(),
                    'avg_guests_by_gender': guest_full.groupby('gender')['id_guest'].nunique().to_dict()
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in complex analysis: {str(e)}")