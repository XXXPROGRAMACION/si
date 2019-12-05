DROP INDEX IF EXISTS index_orderdetail_orderid;
DROP INDEX IF EXISTS index_orders_orderdate;
CREATE INDEX index_orderdetail_orderid ON orderdetail(orderid);

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
		o.orderdate>='2015-04-01'
		AND o.orderdate<='2015-04-30'
	GROUP BY o.customerid
	HAVING SUM(od.price*od.quantity)>100
) AS filtered_customers;