CREATE TABLE medicine_order(
    id SERIAL PRIMARY KEY,
    prescription_id INTEGER NOT NULL REFERENCES prescription(id),
    client_id INTEGER NOT NULL REFERENCES client(id), 
    order_number INTEGER NOT NULL CHECK (order_number > 0),
    order_date DATE NOT NULL CHECK (order_date <= CURRENT_DATE),
    status order_status NOT NULL,
    date_of_issue DATE NULL CHECK (
        date_of_issue IS NULL OR 
        date_of_issue <= CURRENT_DATE
    ),
    production_time INTERVAL CHECK (production_time >= 0),
    cost NUMERIC(10, 2) NOT NULL CHECK (cost > 0)
);