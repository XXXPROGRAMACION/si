-- UPDATE orders SET net_amount=NULL, total_amount=NULL;
CREATE OR REPLACE VIEW orders_details_net_amount AS SELECT order_id, SUM(price*quantity) AS net_amount FROM orders_details GROUP BY order_id;
CREATE OR REPLACE FUNCTION setOrderAmount() RETURNS void AS $$
    UPDATE orders AS o SET
        net_amount=odn.net_amount,
        total_amount=ROUND(CAST(odn.net_amount*(100+o.tax)/100 AS numeric), 2)
        FROM orders_details_net_amount AS odn
        WHERE o.net_amount IS NULL AND o.order_id=odn.order_id;
$$ LANGUAGE sql;
SELECT setOrderAmount();
-- SELECT * FROM orders;