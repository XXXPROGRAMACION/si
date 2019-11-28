CREATE OR REPLACE FUNCTION updInventoryFunction()
RETURNS trigger AS $$ BEGIN
    IF NEW.status<>'Paid' OR OLD.status IS NOT NULL THEN
	    RETURN NULL;
    END IF;

    IF EXISTS (
        SELECT * FROM inventory AS i JOIN (
            SELECT od.product_id, od.quantity 
                FROM orderdetail AS od WHERE od.order_id=OLD.order_id
        ) AS od ON i.product_id=od.product_id WHERE i.stock<od.quantity
    ) THEN
        RETURN NULL;
    END IF;

    INSERT INTO alerts SELECT i.product_id FROM inventory AS i JOIN (
        SELECT od.product_id, od.quantity FROM orderdetail AS od WHERE od.order_id=OLD.order_id
    ) AS od ON i.product_id=od.product_id WHERE i.stock<od.quantity;

    UPDATE inventory AS i SET stock=i.stock-od.quantity
        FROM (SELECT od.product_id, od.quantity FROM orderdetail AS od WHERE od.order_id=OLD.order_id) AS od
        WHERE i.product_id=od.product_id;

    RETURN NEW;
END $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS updInventory ON orders;
CREATE TRIGGER updInventory BEFORE UPDATE ON orders FOR EACH ROW EXECUTE PROCEDURE updInventoryFunction();

--SELECT * FROM orders WHERE status<>'Paid';
--UPDATE orders SET status='Paid' WHERE orderid=88699;