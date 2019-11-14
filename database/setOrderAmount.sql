UPDATE orders SET netamount=NULL, totalamount=NULL;
CREATE OR REPLACE VIEW orderdetail_netamount AS SELECT orderid, SUM(price*quantity) AS netamount FROM orderdetail GROUP BY orderid;
CREATE OR REPLACE FUNCTION setOrderAmount() RETURNS void AS $$
    UPDATE orders AS o SET netamount=odn.netamount, totalamount=ROUND(CAST(odn.netamount*(100+o.tax)/100 AS numeric), 2)
	FROM orderdetail_netamount AS odn WHERE o.netamount IS NULL AND o.orderid=odn.orderid;
$$ LANGUAGE sql;
-- SELECT setOrderAmount();
-- SELECT * FROM orders;