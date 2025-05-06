CREATE TABLE composition (
    medicine_id INTEGER NOT NULL, 
    ingredient_id INTEGER NOT NULL, 
    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),  

    PRIMARY KEY (medicine_id, ingredient_id),  

    FOREIGN KEY (medicine_id)
        REFERENCES medicine(id)
        ON DELETE CASCADE,
        
    FOREIGN KEY (ingredient_id)
        REFERENCES ingredient(id)
        ON DELETE RESTRICT
);