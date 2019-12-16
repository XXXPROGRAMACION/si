DROP INDEX IF EXISTS index_orderdetail_orderid;
DROP INDEX IF EXISTS index_orders_orderdate;

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

-- Explain:
-- Aggregate  (cost=30276.65..30276.66 rows=1 width=8)
--  -> Finalize GroupAggregate  (cost=30275.08..30276.58 rows=5 width=36)
--     Group Key: o.customerid
--     Filter: (sum((od.price * (od.quantity)::numeric)) > '100'::numeric)
--      -> Gather Merge  (cost=30275.08..30276.45 rows=10 width=36)
--         Workers Planned: 2
--          -> Partial GroupAggregate  (cost=29275.05..29275.27 rows=5 width=36)
--             Group Key: o.customerid
--              -> Sort  (cost=29275.05..29275.08 rows=12 width=14)
--                 Sort Key: o.customerid
--                  -> Hash Join  (cost=5866.81..29274.84 rows=12 width=14)
--                     Hash Cond: (od.orderid = o.orderid)
--                      -> Parallel Seq Scan on orderdetail od  (cost=0.00..22314.13 rows=416713 width=14)
--                      -> Hash  (cost=5866.75..5866.75 rows=5 width=8)
--                          ->  Seq Scan on orders o  (cost=0.00..5866.75 rows=5 width=8)
--                              Filter: ((date_part('year'::text, (orderdate)::timestamp without time zone) = '2015'::double precision) AND (date_part('month'::text, (orderdate)::timestamp without time zone) = '4'::double precision))