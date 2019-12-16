EXPLAIN SELECT customerid
FROM customers
EXCEPT
    SELECT customerid
    FROM orders
    WHERE status='Paid';

-- HashSetOp Except  (cost=0.00..4490.42 rows=14093 width=8)
--  -> Append  (cost=0.00..4409.99 rows=32169 width=8)
--      -> Subquery Scan on "*SELECT* 1"  (cost=0.00..634.86 rows=14093 width=8)
--          -> Seq Scan on customers  (cost=0.00..493.93 rows=14093 width=4)
--      -> Subquery Scan on "*SELECT* 2"  (cost=0.00..3775.14 rows=18076 width=8)
--          -> Seq Scan on orders  (cost=0.00..3594.38 rows=18076 width=4)
--             Filter: ((status)::text = 'Paid'::text)