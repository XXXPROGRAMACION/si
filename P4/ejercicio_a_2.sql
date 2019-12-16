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
		EXTRACT(YEAR FROM o.orderdate)='2015'
		AND EXTRACT(MONTH FROM o.orderdate)='04'
	GROUP BY o.customerid
	HAVING SUM(od.price*od.quantity)>100
) AS filtered_customers;

-- Explain:
-- Aggregate  (cost=5093.37..5093.38 rows=1 width=8)
--  -> Finalize GroupAggregate  (cost=5093.20..5093.31 rows=5 width=36)
--     Group Key: o.customerid
--     Filter: (sum((od.price * (od.quantity)::numeric)) > '100'::numeric)
--      -> Sort  (cost=5093.20..5093.21 rows=5 width=36)
--         Sort Key: o.customerid
--          -> Gather  (cost=5092.38..5093.14 rows=5 width=36)
--             Workers Planned: 1
--              -> Partial GroupAggregate  (cost=4092.38..4092.64 rows=5 width=36)
--                 Group Key: o.customerid
--                  -> Sort  (cost=4092.38..4092.42 rows=16 width=14)
--                     Sort Key: o.customerid
--                      -> Nested Loop  (cost=4.48..4092.06 rows=16 width=14)
--                          -> Parallel Seq Scan on orders o  (cost=0.00..3995.38 rows=3 width=8)
--                             Filter: ((date_part('year'::text, (orderdate)::timestamp without time zone) = '2015'::double precision) AND (date_part('month'::text, (orderdate)::timestamp without time zone) = '4'::double precision))
--                              -> Bitmap Heap Scan on orderdetail od  (cost=4.48..32.15 rows=7 width=14)
--                                 Recheck Cond: (orderid = o.orderid)
--                                  -> Bitmap Index Scan on index_orderdetail_orderid  (cost=0.00..4.48 rows=7 width=0)
--                                     Index Cond: (orderid = o.orderid)