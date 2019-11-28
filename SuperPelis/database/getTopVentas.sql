CREATE OR REPLACE VIEW movie_sales AS
SELECT
	movie_id,
	COUNT(movie_id) AS sales
FROM
	orders_details AS od
	JOIN products AS p
	ON od.product_id=p.product_id
GROUP BY movie_id;

CREATE OR REPLACE FUNCTION getTopVentas(
	min_year integer
) RETURNS TABLE (
	year integer,
	title character varying(255),
	sales bigint
) AS $$ BEGIN
	RETURN QUERY
		SELECT 
			ys.year,
			m.title,
			ms.sales
		FROM
			movie_sales AS ms
			JOIN movies AS m
			ON ms.movie_id=m.movie_id
			JOIN (
				SELECT
					m.year,
					MAX(ms.sales) AS sales
				FROM
					movie_sales AS ms
					JOIN movies AS m
					ON ms.movie_id=m.movie_id
				WHERE m.year>=min_year
				GROUP BY m.year
			) AS ys
		ON
			ms.sales=ys.sales
			AND m.year=ys.year
		ORDER BY year ASC;
END $$ LANGUAGE plpgsql;

-- SELECT * FROM getTopVentas(1990);