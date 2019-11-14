CREATE OR REPLACE VIEW months_totalamount AS
SELECT EXTRACT(year FROM orderdate) AS year, EXTRACT(month FROM orderdate) AS month, SUM(totalamount) AS totalamount
FROM orders GROUP BY year, month ORDER BY year, month;

CREATE OR REPLACE VIEW months_products AS
SELECT EXTRACT(year FROM orderdate) AS year, EXTRACT(month FROM orderdate) AS month, SUM(quantity) AS products
FROM orders AS o JOIN orderdetail AS od ON o.orderid=od.orderid GROUP BY year, month ORDER BY year, month;

CREATE OR REPLACE FUNCTION getTopVentas(min_totalamount int, min_products int) RETURNS TABLE (year double precision, month double precision, totalamount numeric, products bigint) AS $$ BEGIN
	RETURN QUERY
		SELECT mta.year, mta.month, mta.totalamount, mp.products
		FROM months_totalamount AS mta JOIN months_products AS mp ON mta.year=mp.year AND mta.month=mp.month
		WHERE mta.totalamount>=min_totalamount OR mp.products>=min_products ORDER BY mta.year, mta.month;
END $$ LANGUAGE plpgsql;

SELECT * FROM getTopVentas(320000, 19000);