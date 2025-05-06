CREATE TABLE medication_delivery(
    id SERIAL PRIMARY KEY,
    medication_id INTEGER NOT NULL,
    application_date DATE NOT NULL CHECK (application_date <= CURRENT_DATE),  
    delivery_date DATE NULL CHECK (
        delivery_date IS NULL OR 
        delivery_date <= CURRENT_DATE
    ),
    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
    
    FOREIGN KEY (medication_id)
        REFERENCES medication(id)
        ON DELETE RESTRICT  
);