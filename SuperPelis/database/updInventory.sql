CREATE OR REPLACE FUNCTION updInventoryFunction()
RETURNS trigger AS $$ BEGIN
    IF NEW.status<>'Paid' OR OLD.status IS NOT NULL THEN
	    RETURN NULL;
    END IF;

    IF EXISTS (
        SELECT *
        FROM
            inventory AS i
            JOIN (
                SELECT
                    od.product_id,
                    od.quantity 
                FROM orders_details AS od
                WHERE od.order_id=OLD.order_id
            ) AS od
            ON i.product_id=od.product_id
            WHERE i.stock<od.quantity
    ) THEN
        RETURN NULL;
    END IF;

    INSERT INTO alerts
    SELECT i.product_id
    FROM
        inventory AS i
        JOIN (
            SELECT
                od.product_id,
                od.quantity
            FROM orders_details AS od
            WHERE od.order_id=OLD.order_id
        ) AS od
        ON i.product_id=od.product_id WHERE i.stock<od.quantity;

    UPDATE inventory AS i
    SET stock=i.stock-od.quantity
    FROM (
        SELECT
            od.product_id,
            od.quantity
        FROM orders_details AS od
        WHERE od.order_id=OLD.order_id
    ) AS od
    WHERE i.product_id=od.product_id;

    RETURN NEW;
END $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS updInventory
ON orders;

CREATE TRIGGER updInventory
BEFORE UPDATE
ON orders
FOR EACH ROW
EXECUTE PROCEDURE updInventoryFunction();

-- SELECT * FROM orders_details WHERE order_id=88699;
-- product_id: 3745
-- quantity: 4
-- SELECT * FROM inventory WHERE product_id=3745;
-- stock: 983
-- UPDATE orders SET status='Paid' WHERE order_id=88699;
-- SELECT * FROM inventory WHERE product_id=3745;
-- stock: 979 (-4)