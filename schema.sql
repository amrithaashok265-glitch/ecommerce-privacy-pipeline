DROP VIEW IF EXISTS v_analytics_customer_orders;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

-- 1. Secured Customer Master Table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,               
    country TEXT,
    country_std TEXT,
    hashed_phone TEXT NOT NULL,       -- Secure Analytical Join Key (SHA-256)
    encrypted_phone TEXT NOT NULL     -- Operational Reversible Key (Fernet)
);

-- 2. Orders Transactional Fact Table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    order_amount REAL,
    delivery_status TEXT,
    delivery_address TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

-- 3. Secure Analytics View Boundary (Exposes columns for LTV calculation while masking PII)
CREATE VIEW v_analytics_customer_orders AS
SELECT 
    c.customer_id,
    c.customer_name,                  
    c.country_std,
    c.hashed_phone,
    o.order_id,
    o.order_date,
    o.order_amount,                   -- Essential for Lifetime Value (LTV) calculation
    o.delivery_status
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;