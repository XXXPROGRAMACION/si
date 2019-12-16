EXPLAIN SELECT customerid
FROM customers
WHERE customerid NOT IN (
    SELECT customerid
    FROM orders
    WHERE status='Paid'
);

-- Explain:
-- Seq Scan on customers  (cost=3639.57..4168.73 rows=7046 width=4)
-- Filter: (NOT (hashed SubPlan 1))
-- SubPlan 1
--  -> Seq Scan on orders  (cost=0.00..3594.38 rows=18076 width=4)
--     Filter: ((status)::text = 'Paid'::text)