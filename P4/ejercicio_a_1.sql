DROP INDEX IF EXISTS index_orders_customerid;
DROP INDEX IF EXISTS index_orders_totalamount;

EXPLAIN SELECT DISTINCT
	o.customerid AS customer_id
FROM orders AS o
WHERE
	o.totalamount>100
	AND EXTRACT(YEAR FROM o.orderdate)='2015'
	AND EXTRACT(MONTH FROM o.orderdate)='04'
;