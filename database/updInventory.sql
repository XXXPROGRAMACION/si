-- MOVER A ACTUALIZA.SQL
-- MOVER A ACTUALIZA.SQL
-- MOVER A ACTUALIZA.SQL
-- MOVER A ACTUALIZA.SQL
-- MOVER A ACTUALIZA.SQL
-- MOVER A ACTUALIZA.SQL
-- MOVER A ACTUALIZA.SQL
-- New table for stock alerts
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL NOT NULL PRIMARY KEY,
    prod_id INTEGER NOT NULL,
    FOREIGN KEY (prod_id) REFERENCES products(prod_id) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION updInventoryFunction()
RETURNS trigger AS $$ BEGIN
    IF NEW.status<>'Paid' OR OLD.status IS NOT NULL THEN
	RETURN NULL;
    END IF;

    IF EXISTS (
        SELECT * FROM inventory AS i JOIN (
            SELECT od.prod_id, od.quantity 
            FROM orderdetail AS od WHERE od.orderid=OLD.orderid
        ) AS od ON i.prod_id=od.prod_id WHERE i.stock<od.quantity
    ) THEN
        RETURN NULL;
    END IF;

    INSERT INTO alerts SELECT i.prod_id FROM inventory AS i JOIN (
        SELECT od.prod_id, od.quantity 
        FROM orderdetail AS od WHERE od.orderid=OLD.orderid
    ) AS od ON i.prod_id=od.prod_id WHERE i.stock<od.quantity;

    UPDATE inventory AS i SET stock=i.stock-od.quantity
    FROM (SELECT od.prod_id, od.quantity FROM orderdetail AS od WHERE od.orderid=OLD.orderid) AS od
    WHERE i.prod_id=od.prod_id;

    RETURN NEW;
END $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS updInventory ON orders;
CREATE TRIGGER updInventory BEFORE UPDATE ON orders
FOR EACH ROW EXECUTE PROCEDURE updInventoryFunction();

--SELECT * FROM orders WHERE status<>'Paid';
--UPDATE orders SET status='Paid' WHERE orderid=88699;