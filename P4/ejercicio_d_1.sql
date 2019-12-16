EXPLAIN SELECT COUNT(*)
FROM orders
WHERE status IS NULL;

-- Base de datos limpia. Explain:
-- HashSetOp Except  (cost=0.00..4490.42 rows=14093 width=8)"
--  -> Append  (cost=0.00..4409.99 rows=32169 width=8)"
--      -> Subquery Scan on "*SELECT* 1"  (cost=0.00..634.86 rows=14093 width=8)"
--          -> Seq Scan on customers  (cost=0.00..493.93 rows=14093 width=4)"
--      -> Subquery Scan on "*SELECT* 2"  (cost=0.00..3775.14 rows=18076 width=8)"
--          -> Seq Scan on orders  (cost=0.00..3594.38 rows=18076 width=4)"
--             Filter: ((status)::text = 'Paid'::text)"

CREATE INDEX index_orders_status ON orders(status);

-- Índice orders(status). Explain:
-- Aggregate  (cost=39.35..39.36 rows=1 width=8)
--  -> Index Only Scan using index_orders_status on orders  (cost=0.42..39.32 rows=12 width=0)
--     Index Cond: (status IS NULL)

EXPLAIN orders;

-- Explain orders. Explain:
-- Aggregate  (cost=22.63..22.64 rows=1 width=8)
--  -> Index Only Scan using index_orders_status on orders  (cost=0.42..22.62 rows=6 width=0)
--     Index Cond: (status IS NULL)