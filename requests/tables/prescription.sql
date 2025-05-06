CREATE TABLE prescription(
    id SERIAL PRIMARY KEY, 
    medicine_id INTEGER NOT NULL REFERENCES medicine(id),
    prescription_number INTEGER NOT NULL CHECK (prescription_number > 0), 
    doctor_surname VARCHAR(50) NOT NULL,
    doctor_name VARCHAR(50) NOT NULL,
    doctor_patronymic VARCHAR(50), 
    signature BYTEA NOT NULL,
    stamp BYTEA NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 0), 
    diagnosis VARCHAR(100) NOT NULL, 
    ammount NUMERIC(10, 2) NOT NULL CHECK (ammount > 0),
    application VARCHAR(100) NOT NULL
);