ALTER TABLE orderdetail
ADD CONSTRAINT orderdetail_orderid_fkey
    FOREIGN KEY (orderid)
    REFERENCES orders(orderid);

ALTER TABLE orders
ADD CONSTRAINT orders_customerid_fkey
    FOREIGN KEY (customerid)
    REFERENCES customers(customerid);