DROP INDEX IF EXISTS index_orders_totalamount;
DROP INDEX IF EXISTS index_orders_orderdate;
DROP INDEX IF EXISTS index_orders_customerid;
CREATE INDEX index_orders_customerid ON orders(customerid);

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
-- Aggregate (cost=5262.85..5262.86 rows=1 width=8)
--  -> Unique (cost=5262.83..5262.84 rows=1 width=4)
--      -> Sort (cost=5262.83..5262.84 rows=1 width=4)
--         Sort Key: o.customerid
--          -> Gather (cost=1000.00..5262.82 rows=1 width=4)
--             Workers Planned: 1
--              -> Parallel Seq Scan on orders o  (cost=0.00..4262.72 rows=1 width=4)
--                 Filter: ((totalamount > '100'::numeric) AND (date_part('year'::text, (orderdate)::timestamp without time zone) = '2015'::double precision) AND (date_part('month'::text, (orderdate)::timestamp without time zone) = '4'::double precision))