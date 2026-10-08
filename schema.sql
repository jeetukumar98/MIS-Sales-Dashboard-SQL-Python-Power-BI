-- MIS Sales Project: MySQL schema
CREATE DATABASE IF NOT EXISTS mis_sales;
USE mis_sales;

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id   INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city          VARCHAR(50),
    state         VARCHAR(50),
    segment       VARCHAR(20),
    join_date     DATE
);

CREATE TABLE products (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(100),
    category     VARCHAR(50),
    unit_price   DECIMAL(10,2),
    cost_price   DECIMAL(10,2)
);

CREATE TABLE sales (
    order_id       INT PRIMARY KEY,
    order_date     DATE,
    customer_id    INT,
    product_id     INT,
    quantity       INT,
    discount_pct   INT,
    total_amount   DECIMAL(12,2),
    payment_mode   VARCHAR(20),
    payment_status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id)
);

CREATE TABLE expenses (
    expense_id   INT PRIMARY KEY,
    expense_date DATE,
    category     VARCHAR(50),
    amount       DECIMAL(12,2)
);

-- Power BI ke liye ready view
CREATE OR REPLACE VIEW vw_sales_report AS
SELECT
    s.order_id,
    s.order_date,
    YEAR(s.order_date)        AS year,
    MONTH(s.order_date)       AS month_no,
    MONTHNAME(s.order_date)   AS month_name,
    c.customer_name,
    c.city,
    c.state,
    c.segment,
    p.product_name,
    p.category,
    s.quantity,
    s.discount_pct,
    s.total_amount,
    (s.total_amount - p.cost_price * s.quantity) AS profit,
    s.payment_mode,
    s.payment_status
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
JOIN products  p ON s.product_id  = p.product_id;

-- Practice queries
-- 1) Monthly revenue
-- SELECT year, month_no, SUM(total_amount) AS revenue FROM vw_sales_report GROUP BY year, month_no ORDER BY year, month_no;
-- 2) Top 5 products by profit
-- SELECT product_name, SUM(profit) AS profit FROM vw_sales_report GROUP BY product_name ORDER BY profit DESC LIMIT 5;
-- 3) Pending payments city-wise
-- SELECT city, SUM(total_amount) AS pending FROM vw_sales_report WHERE payment_status <> 'Paid' GROUP BY city ORDER BY pending DESC;
