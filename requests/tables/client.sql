CREATE TABLE client(
    id SERIAL PRIMARY KEY, 
    surname VARCHAR(50) NOT NULL, 
    name VARCHAR(50) NOT NULL,
    patronymic VARCHAR(50), 
    phone_number VARCHAR(15) NOT NULL
);