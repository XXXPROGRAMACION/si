EXPLAIN SELECT customerid
FROM (
    SELECT customerid
    FROM customers
    UNION ALL
    SELECT customerid
    FROM orders
    WHERE status='Paid'
) AS a
GROUP BY customerid
HAVING COUNT(*)=1;

-- HashAggregate  (cost=4429.91..4431.91 rows=200 width=4)
-- Group Key: customers.customerid
-- Filter: (count(*) = 1)
--  -> Append  (cost=0.00..4269.07 rows=32169 width=4)
--      -> Seq Scan on customers  (cost=0.00..493.93 rows=14093 width=4)
--      -> Seq Scan on orders  (cost=0.00..3594.38 rows=18076 width=4)
--         Filter: ((status)::text = 'Paid'::text)