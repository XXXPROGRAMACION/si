-- Consulta
SELECT COUNT(*)
FROM (
	SELECT DISTINCT
		o.customerid AS customer_id
	FROM orders AS o
	WHERE
		o.totalamount>100
		AND EXTRACT(YEAR FROM o.orderdate)='2015'
		AND EXTRACT(MONTH FROM o.orderdate)='04'
) AS filtered_customers;

-- Índice sobre la columna totalamount de la tabla orders
CREATE INDEX index_orders_totalamount ON orders(totalamount);

-- Índice sobre la columna orderdate de la tabla orders
CREATE INDEX index_orders_orderdate ON orders(orderdate);

-- Índice sobre la columna customerid de la tabla orders
CREATE INDEX index_orders_customerid ON orders(customerid);