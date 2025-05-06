CREATE TABLE ingredient (
    type VARCHAR(100) NOT NULL, 
    caution TEXT NOT NULL, 
    incompatibillity VARCHAR(250) 
) INHERITS (medication);