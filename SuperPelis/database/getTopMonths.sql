CREATE OR REPLACE VIEW months_total_amount AS
SELECT 
	EXTRACT(year FROM date) AS year,
	EXTRACT(month FROM date) AS month,
	SUM(total_amount) AS total_amount 
FROM orders
GROUP BY year, month
ORDER BY year, month;

CREATE OR REPLACE VIEW months_products AS
SELECT
	EXTRACT(year FROM date) AS year,
	EXTRACT(month FROM date) AS month,
	SUM(quantity) AS products
FROM 
	orders AS o
	JOIN orders_details AS od
	ON o.order_id=od.order_id
GROUP BY year, month
ORDER BY year, month;

CREATE OR REPLACE FUNCTION getTopMonths(
	min_total_amount int,
	min_products int
) RETURNS TABLE (
	year integer,
	month integer,
	total_amount numeric,
	products bigint
) AS $$ BEGIN
	RETURN QUERY
		SELECT
			CAST(mta.year AS integer),
			CAST(mta.month AS integer),
			mta.total_amount,
			mp.products
		FROM
			months_total_amount AS mta
			JOIN months_products AS mp
			ON
				mta.year=mp.year
				AND mta.month=mp.month
		WHERE
			mta.total_amount>=min_total_amount
			OR mp.products>=min_products
		ORDER BY mta.year, mta.month;
END $$ LANGUAGE plpgsql;

-- SELECT * FROM getTopMonths(320000, 19000);