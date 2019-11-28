-- Pone el precio base en todas las entradas
UPDATE orders_details AS od SET price=p.price FROM products AS p WHERE od.product_id=p.product_id;
-- Divide por 1.02 tantas veces como años hayan pasado desde la compra
UPDATE orders_details AS od SET price=ROUND(CAST(od.price/POW(1.02, 2019-EXTRACT(year from o.date)) AS numeric), 2)
    FROM orders AS o WHERE od.order_id=o.order_id;
-- Comprobación (Base/2019=12, 2018=11.76, 2017=11.53, 2014=10.87)
-- SELECT p.product_id, od.price AS real_price, p.price AS base_price, od.date
-- FROM (SELECT * FROM orders_details AS od INNER JOIN orders as o ON od.order_id=o.order_id) as od
-- NNER JOIN products AS p ON od.product_id=p.product_id WHERE p.product_id=4000;