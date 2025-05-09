from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .initdb import init_db
from .routers import (
    queries, medication, medicine, technology, ingredient,
    composition, order, client, delivery, inventory, prescription
)

# Initialize the database
init_db()

# Create FastAPI app
app = FastAPI(
    title="Pharmacy API",
    description="API for pharmacy management system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Pharmacy API"}

# Include routers
app.include_router(queries.router)
app.include_router(medication.router)
app.include_router(medicine.router)
app.include_router(technology.router)
app.include_router(ingredient.router)
app.include_router(composition.router)
app.include_router(order.router)
app.include_router(client.router)
app.include_router(delivery.router)
app.include_router(inventory.router)
app.include_router(prescription.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
