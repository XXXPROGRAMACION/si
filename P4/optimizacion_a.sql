-- ESTABLECER PRECIOS
UPDATE orderdetail AS od
SET price=p.price
FROM products AS p
WHERE od.prod_id=p.prod_id;
UPDATE orderdetail AS od
SET price=ROUND(
    CAST(
        od.price/POW(
            1.02,
            2019-EXTRACT(year from o.orderdate)
        ) AS numeric
    ),
    2
)
FROM orders AS o
WHERE od.orderid=o.orderid;