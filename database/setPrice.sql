-- Pone el precio base en todas las entradas
UPDATE orderdetail AS od SET price=p.price FROM products AS p WHERE od.prod_id=p.prod_id;
-- Divide por 1.02 tantas veces como años hayan pasado desde la compra
UPDATE orderdetail AS od SET price=ROUND(CAST(od.price/POW(1.02, 2019-EXTRACT(year from o.orderdate)) AS numeric), 2)
FROM orders AS o WHERE od.orderid=o.orderid;
-- Comprobación (Base/2019=12, 2018=11.764..., 2017=11.534..., 2014=10.868)
-- SELECT p.prod_id, od.price AS real_price, p.price AS base_price, od.orderdate as date
-- FROM (SELECT * FROM orderdetail AS od INNER JOIN orders as o ON od.orderid=o.orderid) as od
-- INNER JOIN products AS p ON od.prod_id=p.prod_id WHERE p.prod_id=4000;