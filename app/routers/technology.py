from fastapi import APIRouter, HTTPException
from typing import List

from ..models import Technology
from .queries import model_to_dict

router = APIRouter(
    prefix="/technologies",
    tags=["technologies"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[dict])
async def read_technologies():
    """
    Get all technologies of preparation.
    """
    technologies = Technology.get_all()
    return [model_to_dict(technology) for technology in technologies]

@router.get("/{technology_id}", response_model=dict)
async def read_technology(technology_id: int):
    """
    Get a specific technology of preparation by ID.
    """
    technology = Technology.get_by_id(technology_id)
    if technology is None:
        raise HTTPException(status_code=404, detail="Technology of preparation not found")
    return model_to_dict(technology)