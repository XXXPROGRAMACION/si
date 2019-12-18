EXPLAIN SELECT COUNT(*)
FROM orders
WHERE status IS NULL;

-- Base de datos limpia. Explain:
-- Aggregate  (cost=3139.91..3139.93 rows=1 width=8)
--  -> Seq Scan on orders  (cost=0.00..3139.90 rows=6 width=0)
--     Filter: (status IS NULL)

CREATE INDEX index_orders_status ON orders(status);

-- Índice orders(status). Explain:
-- Aggregate  (cost=39.35..39.36 rows=1 width=8)
--  -> Index Only Scan using index_orders_status on orders  (cost=0.42..39.32 rows=12 width=0)
--     Index Cond: (status IS NULL)

ANALYZE orders;

-- Analyze orders. Explain:
-- Aggregate  (cost=22.63..22.64 rows=1 width=8)
--  -> Index Only Scan using index_orders_status on orders  (cost=0.42..22.62 rows=6 width=0)
--     Index Cond: (status IS NULL)