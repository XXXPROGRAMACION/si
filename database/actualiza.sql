-- Movies
ALTER TABLE imdb_movies RENAME TO movies;
ALTER TABLE movies RENAME COLUMN movieid TO movie_id;
ALTER TABLE movies RENAME COLUMN movietitle TO title;
UPDATE movies SET year='1998' WHERE year='1998-1999';
ALTER TABLE movies ALTER COLUMN year SET DATA TYPE integer USING year::integer;
ALTER TABLE movies DROP COLUMN movierelease;
ALTER TABLE movies DROP COLUMN movietype;
ALTER TABLE movies DROP COLUMN issuspended;

-- Actors not used
DROP TABLE imdb_actormovies;
DROP TABLE imdb_actors;

-- Directors not used
DROP TABLE imdb_directormovies;
DROP TABLE imdb_directors;

-- Countries
CREATE TABLE countries (
    country_id SERIAL NOT NULL PRIMARY KEY,
    name character varying(32) COLLATE pg_catalog."default" NOT NULL UNIQUE
);

ALTER TABLE imdb_moviecountries RENAME TO movie_countries;
INSERT INTO countries(name) SELECT DISTINCT country FROM movie_countries;

ALTER TABLE movie_countries ADD COLUMN country_id integer;
UPDATE movie_countries AS mc SET country_id=c.country_id FROM countries as c WHERE mc.country=c.name;
ALTER TABLE movie_countries ALTER COLUMN country_id SET NOT NULL;
ALTER TABLE movie_countries ADD CONSTRAINT country_fk FOREIGN KEY (country_id) REFERENCES countries(country_id) ON DELETE CASCADE;

ALTER TABLE movie_countries DROP COLUMN country;

-- Genres
CREATE TABLE genres (
    genre_id SERIAL NOT NULL PRIMARY KEY,
    name character varying(32) COLLATE pg_catalog."default" NOT NULL UNIQUE
);

ALTER TABLE imdb_moviegenres RENAME TO movie_genres;
INSERT INTO genres(name) SELECT DISTINCT genre FROM movie_genres;

ALTER TABLE movie_genres ADD COLUMN genre_id integer;
UPDATE movie_genres AS mg SET genre_id=g.genre_id FROM genres as g WHERE mg.genre=g.name;
ALTER TABLE movie_genres ALTER COLUMN genre_id SET NOT NULL;
ALTER TABLE movie_genres ADD CONSTRAINT genre_fk FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE;

ALTER TABLE movie_genres DROP COLUMN genre;

-- Languages
CREATE TABLE languages (
    language_id SERIAL NOT NULL PRIMARY KEY,
    name CHARACTER varying(32) COLLATE pg_catalog."default" NOT NULL UNIQUE
);

    ALTER TABLE imdb_movielanguages RENAME TO movie_languages;
INSERT INTO languages(name) SELECT DISTINCT language FROM movie_languages;

ALTER TABLE movie_languages ADD COLUMN language_id integer;
UPDATE movie_languages AS ml SET language_id=l.language_id FROM languages as l WHERE ml.language=l.name;
ALTER TABLE movie_languages ALTER COLUMN language_id SET NOT NULL;
ALTER TABLE movie_languages ADD CONSTRAINT language_fk FOREIGN KEY (language_id) REFERENCES languages(language_id) ON DELETE CASCADE;

ALTER TABLE movie_languages DROP COLUMN language;

-- Users
ALTER TABLE customers RENAME TO users;
ALTER TABLE users RENAME COLUMN customerid TO user_id;
ALTER TABLE users RENAME COLUMN address1 TO address;
ALTER TABLE users RENAME COLUMN creditcard TO bank_account;
ALTER TABLE users DROP COLUMN address2;
ALTER TABLE users DROP COLUMN city;
ALTER TABLE users DROP COLUMN state;
ALTER TABLE users DROP COLUMN zip;
ALTER TABLE users DROP COLUMN country;
ALTER TABLE users DROP COLUMN region;
ALTER TABLE users DROP COLUMN phone;
ALTER TABLE users DROP COLUMN creditcardtype;
ALTER TABLE users DROP COLUMN creditcardexpiration;
ALTER TABLE users DROP COLUMN age;
ALTER TABLE users DROP COLUMN income;

-- Products
ALTER TABLE products RENAME COLUMN prod_id TO product_id;
ALTER TABLE products RENAME COLUMN movieid TO movie_id;

-- Inventory
ALTER TABLE inventory RENAME COLUMN prod_id TO product_id;
ALTER TABLE inventory DROP COLUMN sales;

-- Orders
ALTER TABLE orders RENAME COLUMN orderid TO order_id;
ALTER TABLE orders RENAME COLUMN orderdate TO date;
ALTER TABLE orders RENAME COLUMN customerid TO user_id;
ALTER TABLE orders RENAME COLUMN netamount TO net_amount;
ALTER TABLE orders RENAME COLUMN totalamount TO total_amount;

-- Orders details
ALTER TABLE orderdetail RENAME TO orders_details;
ALTER TABLE orders_details RENAME COLUMN orderid TO order_id;
ALTER TABLE orders_details RENAME COLUMN prod_id TO product_id;

-- New table for stock alerts
CREATE TABLE alerts (
    alert_id SERIAL NOT NULL PRIMARY KEY,
    product_id integer NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);