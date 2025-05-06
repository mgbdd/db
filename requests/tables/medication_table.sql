CREATE TABLE medication (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL, 
    manufacturer VARCHAR(50) NOT NULL, 
    critical_norm NUMERIC(10, 2) NOT NULL,
    shelf_life INTERVAL NOT NULL,
    unit_of_measure units_of_measure NOT NULL,
    units_per_package NUMERIC(10, 2) CHECK (units_per_package > 0),
    price NUMERIC(10, 2) CHECK (price > 0), 
    storage_conditions VARCHAR(250) NOT NULL,
    current_amount NUMERIC(10, 2) CHECK (current_amount >= 0)
);