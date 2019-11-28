CREATE OR REPLACE FUNCTION updOrdersFunction()
RETURNS trigger AS $$
DECLARE
    current_order_id integer := 0;
    new_price numeric := 0;
    new_quantity integer := 0;
    old_price numeric := 0;
    old_quantity integer := 0;
BEGIN
    IF NEW.order_id IS NOT NULL THEN
        current_order_id := NEW.order_id;
    ELSIF OLD.order_id IS NOT NULL THEN
        current_order_id := OLD.order_id;
    ELSE
        RETURN NULL;
    END IF;

    IF NEW.price IS NOT NULL AND NEW.quantity IS NOT NULL THEN
        new_price := NEW.price;
        new_quantity := NEW.quantity;
    END IF;

    IF OLD.price IS NOT NULL AND OLD.quantity IS NOT NULL THEN
        old_price := OLD.price;
        old_quantity := OLD.quantity;
    END IF;

    UPDATE orders AS o SET net_amount=ROUND(CAST(o.net_amount+(new_price*new_quantity)-(old_price*old_quantity) AS numeric), 2) WHERE o.order_id=order_id;
    -- Dos distintas porque o.net_amount en la anterior no está actualizada
    UPDATE orders AS o SET total_amount=ROUND(CAST(o.net_amount*(100+o.tax)/100 AS numeric), 2) WHERE o.order_id=current_order_id;

    RETURN NEW;
END $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS updInventory ON orders_details;
CREATE TRIGGER updInventory BEFORE INSERT OR UPDATE OR DELETE ON orders_details FOR EACH ROW EXECUTE PROCEDURE updOrdersFunction();

-- SELECT * FROM orders WHERE order_id=161010;
-- net_amount: 103.30
-- SELECT * FROM products WHERE product_id=1;
-- price: 13
-- INSERT INTO orders_details (order_id, product_id, price, quantity) VALUES (161010, 1, 13, 2);
-- SELECT * FROM orders WHERE order_id=161010;
-- net_amount: 129.30 (+26)
-- UPDATE orders_details SET quantity=1 WHERE order_id=161010 AND product_id=1;
-- SELECT * FROM orders WHERE order_id=161010;
-- net_amount: 116.30 (-13)
-- DELETE FROM orders_details WHERE order_id=161010 AND product_id=1;
-- SELECT * FROM orders WHERE order_id=161010;
-- net_amount: 103.30 (-13)