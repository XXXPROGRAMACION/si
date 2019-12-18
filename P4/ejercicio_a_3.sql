DROP INDEX IF EXISTS index_orders_customerid;
DROP INDEX IF EXISTS index_orders_totalamount;
CREATE INDEX index_orders_totalamount ON orders(totalamount);

EXPLAIN SELECT DISTINCT
	o.customerid AS customer_id
FROM orders AS o
WHERE
	o.totalamount>100
	AND EXTRACT(YEAR FROM o.orderdate)='2015'
	AND EXTRACT(MONTH FROM o.orderdate)='04'
;

-- Explain:
-- Aggregate  (cost=6549.94..6549.95 rows=1 width=8)
--  -> Finalize GroupAggregate  (cost=6549.79..6549.88 rows=5 width=36)
--     Group Key: o.customerid
--     Filter: (sum(o.totalamount) > '100'::numeric)
--      -> Sort  (cost=6549.79..6549.80 rows=3 width=36)
--         Sort Key: o.customerid
--          -> Gather  (cost=6549.41..6549.77 rows=3 width=36)
--             Workers Planned: 1
--              -> Partial GroupAggregate  (cost=5549.41..5549.47 rows=3 width=36)
--                 Group Key: o.customerid
--                  -> Sort  (cost=5549.41..5549.41 rows=3 width=10)
--                     Sort Key: o.customerid
--                      -> Parallel Seq Scan on orders o  (cost=0.00..5549.38 rows=3 width=10)
--                         Filter: ((date_part('year'::text, (orderdate)::timestamp without time zone) = '2015'::double precision) AND (date_part('month'::text, (orderdate)::timestamp without time zone) = '4'::double precision))