-- ESTABLECER PRECIOS
UPDATE orderdetail AS od
SET price=p.price
FROM products AS p
WHERE od.prod_id=p.prod_id;
UPDATE orderdetail AS od
SET price=ROUND(
    CAST(
        od.price/POW(
            1.02,
            2019-EXTRACT(year from o.orderdate)
        ) AS numeric
    ),
    2
)
FROM orders AS o
WHERE od.orderid=o.orderid;
-- UPDATE orders SET net_amount=NULL, total_amount=NULL;
CREATE OR REPLACE VIEW orderdetail_netamount AS
SELECT
    orderid,
    SUM(price*quantity) AS netamount
FROM orderdetail
GROUP BY orderid;
UPDATE orders AS o
SET
    netamount=odn.netamount,
    totalamount=ROUND(CAST(odn.netamount*(100+o.tax)/100 AS numeric), 2)
FROM orderdetail_netamount AS odn
WHERE
    o.netamount IS NULL
    AND o.orderid=odn.orderid
;