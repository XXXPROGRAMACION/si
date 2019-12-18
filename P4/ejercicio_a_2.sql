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
-- Aggregate (cost=8.48..8.49 rows=1 width=8)
--  -> Unique (cost=8.46..8.47 rows=1 width=4)
--      -> Sort (cost=8.46..8.47 rows=1 width=4)
--         Sort Key: o.customerid
--          -> Index Scan using index_orders_totalamount on orders o  (cost=0.42..8.45 rows=1 width=4)
--             Index Cond: (totalamount > '100'::numeric)
--             Filter: ((date_part('year'::text, (orderdate)::timestamp without time zone) = '2015'::double precision) AND (date_part('month'::text, (orderdate)::timestamp without time zone) = '4'::double precision))