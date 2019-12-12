DROP INDEX IF EXISTS index_orderdetail_orderid;
DROP INDEX IF EXISTS index_orders_orderdate;
CREATE INDEX index_orders_orderdate ON orders(orderdate);

EXPLAIN SELECT COUNT(*)
FROM (
	SELECT
		o.customerid AS customer_id,
		SUM(od.price*od.quantity) AS total_amount
	FROM
		orderdetail AS od
		JOIN orders AS o
		ON od.orderid=o.orderid
	WHERE
		EXTRACT(YEAR FROM o.orderdate)='2015'
		AND EXTRACT(MONTH FROM o.orderdate)='04'
	GROUP BY o.customerid
	HAVING SUM(od.price*od.quantity)>100
) AS filtered_customers;