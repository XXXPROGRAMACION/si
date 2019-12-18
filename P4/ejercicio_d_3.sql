EXPLAIN SELECT COUNT(*)
FROM orders
WHERE status='Paid';

ANALYZE orders;

-- Analyze orders. Explain:
-- Aggregate  (cost=1967.30..1967.31 rows=1 width=8)
--  -> Bitmap Heap Scan on orders  (cost=367.80..1921.05 rows=18500 width=0)
--     Recheck Cond: ((status)::text = 'Paid'::text)
--      -> Bitmap Index Scan on index_orders_status  (cost=0.00..363.17 rows=18500 width=0)
--         Index Cond: ((status)::text = 'Paid'::text)