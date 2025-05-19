from fastapi import APIRouter, HTTPException
from typing import List

from ..models import Ingredient
from .queries import model_to_dict

router = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[dict])
async def read_ingredients():
    """
    Get all ingredients.
    """
    ingredients = Ingredient.get_all()
    return [model_to_dict(ingredient) for ingredient in ingredients]

@router.get("/{ingredient_id}", response_model=dict)
async def read_ingredient(ingredient_id: int):
    """
    Get a specific ingredient by ID.
    """
    ingredient = Ingredient.get_by_id(ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return model_to_dict(ingredient)