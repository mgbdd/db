CREATE TYPE order_status AS ENUM (
    'waiting for a delivery',
    'producing',
    'ready',
    'issued', 
    'cancelled'
);