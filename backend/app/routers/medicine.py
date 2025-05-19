from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import timedelta

from ..models import Medicine, Medication, MedicineType, MedicineKind, MethodOfApplication
from .queries import model_to_dict
from pydantic import BaseModel

router = APIRouter(
    prefix="/medicines",
    tags=["medicines"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[dict])
async def read_medicines():
    """
    Get all medicines.
    """
    medicines = Medicine.get_all()
    return [model_to_dict(medicine) for medicine in medicines]

@router.get("/{medicine_id}", response_model=dict)
async def read_medicine(medicine_id: int):
    """
    Get a specific medicine by ID.
    """
    medicine = Medicine.get_by_id(medicine_id)
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return model_to_dict(medicine)

