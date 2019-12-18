-- Crear nueva columna promo
ALTER TABLE customers
ADD promo numeric;

-- Crear la función de actualización
CREATE OR REPLACE FUNCTION updPromoFunction()
RETURNS trigger AS $$
DECLARE
BEGIN
    IF NEW.promo=OLD.promo THEN
        return NEW;
    END IF;

    PERFORM pg_sleep(10);

    UPDATE orders AS o
    SET totalamount=ROUND(
        CAST(
            o.netamount*(100+o.tax)/100*(100-NEW.promo)/100
            AS numeric
        ),
        2
    )
    WHERE
        o.customerid=NEW.customerid
        AND o.status IS NULL
    ;

    RETURN NEW;
END $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS updPromo
ON customers;

CREATE TRIGGER updPromo
BEFORE UPDATE
ON customers
FOR EACH ROW
EXECUTE PROCEDURE updPromoFunction();

-- Comprobación del correcto funcionamiento del trigger:
-- UPDATE orders SET status=NULL WHERE customerid=3;
-- UPDATE customers SET promo=50 WHERE customerid=3;
-- SELECT * FROM orders WHERE customerid=3;