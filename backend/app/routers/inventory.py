from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import date

from ..models import Inventory, Medication
from .queries import model_to_dict

router = APIRouter(
    prefix="/inventories",
    tags=["inventories"],
    responses={404: {"description": "Not found"}},
)

class InventoryCreate(BaseModel):
    medication_id: int
    date: date
    amount: int

class InventoryUpdate(BaseModel):
    medication_id: Optional[int] = None
    date: Optional[date] = None
    amount: Optional[int] = None

@router.get("/", response_model=List[dict])
async def read_inventories():
    """
    Get all inventories.
    """
    inventories = Inventory.get_all()
    return [model_to_dict(inventory) for inventory in inventories]

@router.get("/{inventory_id}", response_model=dict)
async def read_inventory(inventory_id: int):
    """
    Get a specific inventory by ID.
    """
    inventory = Inventory.get_by_id(inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return model_to_dict(inventory)

@router.post("/", response_model=dict)
async def create_inventory(inventory: InventoryCreate):
    """
    Create a new inventory.
    """
    # Check if medication exists
    medication = Medication.get_by_id(inventory.medication_id)
    if medication is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    
    # Create and save the inventory
    new_inventory = Inventory(
        medication_id=inventory.medication_id,
        date=inventory.date,
        amount=inventory.amount
    )
    new_inventory.save()
    
    return model_to_dict(new_inventory)

@router.put("/{inventory_id}", response_model=dict)
async def update_inventory(inventory_id: int, inventory: InventoryUpdate):
    """
    Update an inventory.
    """
    # Check if inventory exists
    existing_inventory = Inventory.get_by_id(inventory_id)
    if existing_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    # Update inventory fields if provided
    if inventory.medication_id is not None:
        # Check if medication exists
        medication = Medication.get_by_id(inventory.medication_id)
        if medication is None:
            raise HTTPException(status_code=404, detail="Medication not found")
        existing_inventory.medication_id = inventory.medication_id
    
    if inventory.date is not None:
        existing_inventory.date = inventory.date
    
    if inventory.amount is not None:
        existing_inventory.amount = inventory.amount
    
    # Save the updated inventory
    existing_inventory.save()
    
    return model_to_dict(existing_inventory)

@router.delete("/{inventory_id}", status_code=204)
async def delete_inventory(inventory_id: int):
    """
    Delete an inventory.
    """
    # Check if inventory exists
    inventory = Inventory.get_by_id(inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    # Delete the inventory
    from ..database import execute_query
    query = "DELETE FROM inventory WHERE id = %s"
    execute_query(query, (inventory_id,), fetch=False)
    
    return None