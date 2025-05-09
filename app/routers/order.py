from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import date

from ..models import Order, Prescription, Client, OrderStatus
from .queries import model_to_dict

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

class OrderCreate(BaseModel):
    prescription_id: int
    client_id: int
    order_number: int
    order_date: date
    status: str
    date_of_issue: Optional[date] = None
    production_time: Optional[str] = None
    cost: float

class OrderUpdate(BaseModel):
    prescription_id: Optional[int] = None
    client_id: Optional[int] = None
    order_number: Optional[int] = None
    order_date: Optional[date] = None
    status: Optional[str] = None
    date_of_issue: Optional[date] = None
    production_time: Optional[str] = None
    cost: Optional[float] = None

@router.get("/", response_model=List[dict])
async def read_orders():
    """
    Get all orders.
    """
    orders = Order.get_all()
    return [model_to_dict(order) for order in orders]

@router.get("/{order_id}", response_model=dict)
async def read_order(order_id: int):
    """
    Get a specific order by ID.
    """
    order = Order.get_by_id(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return model_to_dict(order)

@router.post("/", response_model=dict)
async def create_order(order: OrderCreate):
    """
    Create a new order.
    """
    # Check if prescription exists
    prescription = Prescription.get_by_id(order.prescription_id)
    if prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    # Check if client exists
    client = Client.get_by_id(order.client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Create and save the order
    new_order = Order(
        prescription_id=order.prescription_id,
        client_id=order.client_id,
        order_number=order.order_number,
        order_date=order.order_date,
        status=order.status,
        date_of_issue=order.date_of_issue,
        production_time=order.production_time,
        cost=order.cost
    )
    new_order.save()
    
    return model_to_dict(new_order)

@router.put("/{order_id}", response_model=dict)
async def update_order(order_id: int, order: OrderUpdate):
    """
    Update an order.
    """
    # Check if order exists
    existing_order = Order.get_by_id(order_id)
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update order fields if provided
    if order.prescription_id is not None:
        # Check if prescription exists
        prescription = Prescription.get_by_id(order.prescription_id)
        if prescription is None:
            raise HTTPException(status_code=404, detail="Prescription not found")
        existing_order.prescription_id = order.prescription_id
    
    if order.client_id is not None:
        # Check if client exists
        client = Client.get_by_id(order.client_id)
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        existing_order.client_id = order.client_id
    
    if order.order_number is not None:
        existing_order.order_number = order.order_number
    
    if order.order_date is not None:
        existing_order.order_date = order.order_date
    
    if order.status is not None:
        existing_order.status = order.status
    
    if order.date_of_issue is not None:
        existing_order.date_of_issue = order.date_of_issue
    
    if order.production_time is not None:
        existing_order.production_time = order.production_time
    
    if order.cost is not None:
        existing_order.cost = order.cost
    
    # Save the updated order
    existing_order.save()
    
    return model_to_dict(existing_order)

@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: int):
    """
    Delete an order.
    """
    # Check if order exists
    order = Order.get_by_id(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Delete the order
    from ..database import execute_query
    query = "DELETE FROM medicine_order WHERE id = %s"
    execute_query(query, (order_id,), fetch=False)
    
    return None