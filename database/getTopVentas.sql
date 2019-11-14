CREATE OR REPLACE VIEW movie_sales AS SELECT movieid, COUNT(movieid) AS sales FROM orderdetail AS od JOIN products AS p ON od.prod_id=p.prod_id GROUP BY movieid;
CREATE OR REPLACE FUNCTION getTopVentas(min_year int) RETURNS TABLE (year text, movietitle character varying (255), sales bigint) LANGUAGE plpgsql AS $$
BEGIN
	RETURN QUERY
		SELECT ys.year, m.movietitle, ms.sales FROM movie_sales AS ms JOIN imdb_movies AS m ON ms.movieid=m.movieid JOIN
		(SELECT m.year, MAX(ms.sales) AS sales FROM movie_sales AS ms JOIN imdb_movies AS m ON ms.movieid=m.movieid WHERE m.year>=CAST(min_year AS text) GROUP BY m.year) AS ys
		ON ms.sales=ys.sales AND m.year=ys.year ORDER BY year ASC;
END
$$;
SELECT * FROM getTopVentas(2000);