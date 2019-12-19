SELECT *
FROM (
	SELECT COUNT(*) AS customers
	FROM customers
	WHERE customerid=100
) AS c, (
	SELECT COUNT(*) AS orders
	FROM orders
	WHERE customerid=100
) AS o, (
	SELECT COUNT(*) AS orderdetail
	FROM
		orderdetail
		NATURAL JOIN orders
	WHERE customerid=100
) AS od;