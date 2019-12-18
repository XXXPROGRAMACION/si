DROP INDEX IF EXISTS index_orders_totalamount;
DROP INDEX IF EXISTS index_orders_orderdate;
DROP INDEX IF EXISTS index_orders_customerid;
CREATE INDEX index_orders_orderdate ON orders(orderdate);

EXPLAIN SELECT COUNT(*)
FROM (
	SELECT DISTINCT
		o.customerid AS customer_id
	FROM orders AS o
	WHERE
		o.totalamount>100
		AND EXTRACT(YEAR FROM o.orderdate)='2015'
		AND EXTRACT(MONTH FROM o.orderdate)='04'
) AS filtered_customers;

-- Explain:
-- Aggregate (cost=6816.97..6816.98 rows=1 width=8)
--  -> Unique (cost=6816.93..6816.94 rows=2 width=4)
--      -> Sort (cost=6816.93..6816.94 rows=2 width=4)
--         Sort Key: o.customerid
--          -> Gather (cost=1000.00..6816.92 rows=2 width=4)
--             Workers Planned: 1
--              -> Parallel Seq Scan on orders o  (cost=0.00..5816.72 rows=1 width=4)
--                 Filter: (...)