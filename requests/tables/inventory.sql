CREATE TABLE inventory(
    id SERIAL PRIMARY KEY,
    medication_id INTEGER NOT NULL,
    date DATE NOT NULL CHECK (date <= CURRENT_DATE), 
    amount INTEGER NOT NULL CHECK (amount >= 0),
    
    FOREIGN KEY (medication_id)
        REFERENCES medication(id)
        ON DELETE RESTRICT
);
