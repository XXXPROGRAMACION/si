EXPLAIN SELECT COUNT(*)
FROM orders
WHERE status='Processed';

EXPLAIN orders;

-- Explain orders. Explain:
-- Aggregate  (cost=2583.36..2583.37 rows=1 width=8)"
--  -> Bitmap Heap Scan on orders  (cost=717.44..2492.71 rows=36261 width=0)"
--     Recheck Cond: ((status)::text = 'Processed'::text)"
--      -> Bitmap Index Scan on index_orders_status  (cost=0.00..708.38 rows=36261 width=0)"
--         Index Cond: ((status)::text = 'Processed'::text)"