CREATE TABLE medicine (
    type medicine_type NOT NULL, 
    kind medicine_kind NOT NULL, 
    application method_of_application NOT NULL, 
    tech_prep_id INTEGER NOT NULL REFERENCES technology_of_preparation(id),
     CONSTRAINT valid_tech_prep CHECK (tech_prep_id > 0)
) INHERITS (medication);