EXPLAIN SELECT COUNT(*)
FROM orders
WHERE status='Shipped';

-- Base de datos limpia. Explain:
-- Finalize Aggregate  (cost=3845.90..3845.91 rows=1 width=8)
--  -> Gather  (cost=3845.78..3845.89 rows=1 width=8)
--     Workers Planned: 1
--      -> Partial Aggregate  (cost=2845.78..2845.79 rows=1 width=8)
--          -> Parallel Seq Scan on orders  (cost=0.00..2658.69 rows=74837 width=0)
--             Filter: ((status)::text = 'Shipped'::text)

CREATE INDEX index_orders_status ON orders(status);

-- Índice orders(status). Explain (igual que sin índice):
-- Finalize Aggregate  (cost=3845.90..3845.91 rows=1 width=8)
--  -> Gather  (cost=3845.78..3845.89 rows=1 width=8)
--     Workers Planned: 1
--      -> Partial Aggregate  (cost=2845.78..2845.79 rows=1 width=8)
--          -> Parallel Seq Scan on orders  (cost=0.00..2658.69 rows=74837 width=0)
--             Filter: ((status)::text = 'Shipped'::text)

ANALYZE orders;

-- Analyze orders. Explain:
-- Finalize Aggregate  (cost=3845.60..3845.61 rows=1 width=8)
--  -> Gather  (cost=3845.49..3845.60 rows=1 width=8)
--     Workers Planned: 1
--      -> Partial Aggregate  (cost=2845.49..2845.50 rows=1 width=8)
--          -> Parallel Seq Scan on orders  (cost=0.00..2658.69 rows=74719 width=0)
--             Filter: ((status)::text = 'Shipped'::text)