UPDATE orders SET netamount=NULL, totalamount=NULL;
CREATE OR REPLACE VIEW orderdetail_netamount AS SELECT orderid, SUM(price) AS netamount FROM orderdetail GROUP BY orderid;
CREATE OR REPLACE PROCEDURE setOrderAmount() LANGUAGE SQL AS
$$
    UPDATE orders AS o SET netamount=odn.netamount, totalamount=odn.netamount*(100+o.tax)/100
	FROM orderdetail_netamount AS odn WHERE o.netamount IS NULL AND o.orderid=odn.orderid;
$$;
CALL setOrderAmount();
SELECT * FROM orders;