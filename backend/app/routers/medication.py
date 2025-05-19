from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Medication
from .queries import model_to_dict

router = APIRouter(
    prefix="/medications",
    tags=["medications"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[dict])
async def read_medications():
    """
    Get all medications.
    """
    medications = Medication.get_all()
    return [model_to_dict(medication) for medication in medications]

@router.get("/{medication_id}", response_model=dict)
async def read_medication(medication_id: int):
    """
    Get a specific medication by ID.
    """
    medication = Medication.get_by_id(medication_id)
    if medication is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    return model_to_dict(medication)
