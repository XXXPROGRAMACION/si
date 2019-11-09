-- Countries
CREATE TABLE countries (
    id SERIAL NOT NULL PRIMARY KEY,
    name CHARACTER VARYING(32) COLLATE pg_catalog."default" NOT NULL UNIQUE
);

INSERT INTO countries(name) SELECT DISTINCT country FROM imdb_moviecountries;

ALTER TABLE imdb_moviecountries ADD COLUMN country_id INTEGER;
UPDATE imdb_moviecountries as mc SET country_id=c.id FROM countries as c WHERE mc.country=c.name;
ALTER TABLE imdb_moviecountries ALTER COLUMN country_id SET NOT NULL;
ALTER TABLE imdb_moviecountries ADD CONSTRAINT country_fk FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE;

ALTER TABLE imdb_moviecountries DROP COLUMN country;

-- Genres
CREATE TABLE genres (
    id SERIAL NOT NULL PRIMARY KEY,
    name CHARACTER VARYING(32) COLLATE pg_catalog."default" NOT NULL UNIQUE
);

INSERT INTO genres(name) SELECT DISTINCT genre FROM imdb_moviegenres;

ALTER TABLE imdb_moviegenres ADD COLUMN genre_id INTEGER;
UPDATE imdb_moviegenres as mg SET genre_id=g.id FROM genres as g WHERE mg.genre=g.name;
ALTER TABLE imdb_moviegenres ALTER COLUMN genre_id SET NOT NULL;
ALTER TABLE imdb_moviegenres ADD CONSTRAINT genre_fk FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE;

ALTER TABLE imdb_moviegenres DROP COLUMN genre;

-- Languages
CREATE TABLE languages (
    id SERIAL NOT NULL PRIMARY KEY,
    name CHARACTER VARYING(32) COLLATE pg_catalog."default" NOT NULL UNIQUE
);

INSERT INTO languages(name) SELECT DISTINCT language FROM imdb_movielanguages;

ALTER TABLE imdb_movielanguages ADD COLUMN language_id INTEGER;
UPDATE imdb_movielanguages as ml SET language_id=l.id FROM languages as l WHERE ml.language=l.name;
ALTER TABLE imdb_movielanguages ALTER COLUMN language_id SET NOT NULL;
ALTER TABLE imdb_movielanguages ADD CONSTRAINT language_fk FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE CASCADE;

ALTER TABLE imdb_movielanguages DROP COLUMN language;
ALTER TABLE imdb_movielanguages DROP COLUMN extrainformation;