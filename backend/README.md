# Pharmacy API

This is a FastAPI-based API for a pharmacy management system. It provides endpoints to access various pharmacy-related data.

## Installation

1. Clone the repository
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the API

To run the API, use one of the following commands:

### Option 1: Using the run_api.py script

```
cd db
python run_api.py
```

### Option 2: Using the module directly

```
cd db
python -m app.main
```

The API will be available at http://localhost:8000

## API Documentation

Once the API is running, you can access the auto-generated documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Available Endpoints

### Clients

- `GET /clients/unclaimed-orders` - Get all clients with unclaimed orders
- `GET /clients/unclaimed-orders/count` - Get the count of clients with unclaimed orders
- `GET /clients/waiting-for-delivery` - Get all clients waiting for delivery
- `GET /clients/waiting-for-delivery/count` - Get the count of clients waiting for delivery
- `GET /clients/waiting-for-delivery/count/{med_type}` - Get the count of clients waiting for delivery by medication type
- `GET /clients/by-medication-name` - Get clients by medication name and period
- `GET /clients/by-medication-type` - Get clients by medication type and period
- `GET /clients/by-medication-name/count` - Get the count of clients by medication name and period
- `GET /clients/by-medication-type/count` - Get the count of clients by medication type and period
- `GET /clients/most-frequent` - Get the most frequent clients

### Medicines

- `GET /medicines/details` - Get all medicine details
- `GET /medicines/details/{medicine_name}` - Get medicine details by name
- `GET /medicines/price-and-components/{medicine_name}` - Get medicine price and components by name

### Medications

- `GET /medications/top` - Get top 10 medications
- `GET /medications/top/{med_type}` - Get top 10 medications by type
- `GET /medications/critical` - Get medications at critical level
- `GET /medications/low-stock` - Get low stock medications
- `GET /medications/low-stock/{med_type}` - Get low stock medications by type

### Ingredients

- `GET /ingredients/usage/{ingredient_name}` - Get ingredient usage volume
- `GET /ingredients/for-producing-orders` - Get ingredients for producing orders
- `GET /ingredients/for-producing-orders/count` - Get the count of ingredients for producing orders

### Orders

- `GET /orders/producing` - Get all producing orders
- `GET /orders/producing/count` - Get the count of producing orders

### Technologies

- `GET /technologies` - Get technologies of preparation

## Query Parameters

Some endpoints require query parameters:

- `start_date` and `end_date` - Date format: YYYY-MM-DD
- `medicine_type` - Type of medicine
- `medicine_names` - List of medicine names
- `from_producing_orders` - Boolean flag
- `limit` - Integer limit for results
