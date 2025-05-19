from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from ..models import Technology
from .queries import model_to_dict

router = APIRouter(
    prefix="/technologies",
    tags=["technologies"],
    responses={404: {"description": "Not found"}},
)

class TechnologyCreate(BaseModel):
    name: str
    description: str

class TecnologyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

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

@router.post("/", response_model=dict)
async def create_technology(technology: TechnologyCreate):
    """
    Create a new technology of preparation.
    """
    new_technology = Technology(
        name=technology.name,
        description=technology.description
    )
    new_technology.save()
    return model_to_dict(new_technology)

@router.put("/{technology_id}", response_model=dict)
async def update_technology(technology_id: int, technology: TecnologyUpdate):
    """
    Update a technology of preparation by ID.
    """
    existing_technology = Technology.get_by_id(technology_id)
    if existing_technology is None:
        raise HTTPException(status_code=404, detail="Technology of preparation not found")
    if technology.name is not None:
        existing_technology.name = technology.name
    if technology.description is not None:
        existing_technology.description = technology.description
    existing_technology.save()
    return model_to_dict(existing_technology)

@router.delete("/{technology_id}", status_code=204)
async def delete_technology(technology_id: int):
    """
    Delete a technology of preparation by ID.
    """
    # Check if technology exists
    technology = Technology.get_by_id(technology_id)
    if technology is None:
        raise HTTPException(status_code=404, detail="Technology of preparation not found")
    
    # Delete the technology
    from ..database import execute_query
    query = "DELETE FROM technology_of_preparation WHERE id = %s"
    execute_query(query, (technology_id,), fetch=False)
    
    return None