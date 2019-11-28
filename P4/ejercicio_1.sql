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

-- CONSULTA
EXPLAIN SELECT COUNT(*)
FROM (
	SELECT
		customerid AS customer_id,
		SUM(price*quantity) AS total_amount
	FROM
		orderdetail AS od
		JOIN orders AS o
		ON od.orderid=o.orderid
	WHERE
		EXTRACT(year FROM orderdate)=2015
		AND EXTRACT(month FROM orderdate)=04
	GROUP BY customerid
	HAVING SUM(price*quantity)>100
) AS filtered_customers;