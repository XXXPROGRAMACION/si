-- Consulta 1
EXPLAIN SELECT COUNT(*)
FROM orders
WHERE status IS NULL;

-- Consulta 2
EXPLAIN SELECT COUNT(*)
FROM orders
WHERE status='Shipped';

-- Consulta 3
EXPLAIN SELECT COUNT(*)
FROM orders
WHERE status='Paid';

-- Consulta 4
EXPLAIN SELECT COUNT(*)
FROM orders
WHERE status='Processed';;

-- Índice sobre la columna status de la tabla orders
CREATE INDEX index_orders_status ON orders(status);

-- Análisis de la tabla orders
ANALYZE orders;