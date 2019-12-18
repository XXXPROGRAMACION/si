DROP INDEX IF EXISTS index_orders_totalamount;
DROP INDEX IF EXISTS index_orders_orderdate;
DROP INDEX IF EXISTS index_orders_customerid;
CREATE INDEX index_orders_totalamount ON orders(totalamount);

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
-- Aggregate (cost=5669.36..5669.37 rows=1 width=8)
--  -> Unique (cost=5669.33..5669.34 rows=2 width=4)
--      -> Sort (cost=5669.33..5669.33 rows=2 width=4)
--         Sort Key: o.customerid
--          -> Bitmap Heap Scan on orders o  (cost=1126.90..5669.32 rows=2 width=4)
--             Recheck Cond: (totalamount > '100'::numeric)
--             Filter: (...)
--              -> Bitmap Index Scan on index_orders_totalamount  (cost=0.00..1126.90 rows=60597 width=0)
--                 Index Cond: (totalamount > '100'::numeric)