# -*- coding: utf-8 -*-

import os
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select
import datetime

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)
# cargar una tabla
db_table_movies = Table('imdb_movies', db_meta, autoload=True, autoload_with=db_engine)

def db_listOfMovies1949():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Seleccionar las peliculas del año 1949
        db_movies_1949 = select([db_table_movies]).where(text("year = '1949'"))
        db_result = db_conn.execute(db_movies_1949)
        #db_result = db_conn.execute("Select * from imdb_movies where year = '1949'")
        
        db_conn.close()
        
        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def latest_movies(amount):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        
        db_result = db_conn.execute("SELECT * FROM imdb_movies AS m JOIN products AS p ON m.movieid=p.movieid ORDER BY year DESC LIMIT " + str(amount))
        
        db_conn.close()
        
        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def search_product(title, amount=50):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        if title is None:
            db_result = db_conn.execute("SELECT * FROM imdb_movies AS m JOIN products AS p ON m.movieid=p.movieid LIMIT " + str(amount))
        else:
            db_result = db_conn.execute("SELECT * FROM imdb_movies AS m JOIN products AS p ON m.movieid=p.movieid WHERE m.movietitle LIKE \'%%" + title + "%%\' LIMIT " + str(amount))
        
        db_conn.close()
        
        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def load_product(product_id):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        db_result = db_conn.execute("SELECT * FROM imdb_movies AS m JOIN products AS p ON m.movieid=p.movieid WHERE p.prod_id=" + str(product_id) + " LIMIT 1")
        
        db_conn.close()
        
        return list(db_result)[0]
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def user_exists(username):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        db_result = db_conn.execute("SELECT * FROM CUSTOMERS AS c WHERE c.username LIKE \'%%" + username + "%%\' LIMIT 1")
        
        db_conn.close()
        
        users = list(db_result)

        for user in users:
            if user.username == username:
                return True

        return False
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def email_exists(email):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        db_result = db_conn.execute("SELECT * FROM CUSTOMERS AS c WHERE c.email LIKE \'%%" + email + "%%\' LIMIT 1")
        
        db_conn.close()

        users = list(db_result)

        for user in users:
            if user.email == email:
                return True

        return False
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def login(username, password):
    if username is None or password is None:
        return None

    if not user_exists(username):
        return None

    try:
        db_conn = None
        db_conn = db_engine.connect()

        db_result = db_conn.execute("SELECT * FROM CUSTOMERS AS c WHERE c.username LIKE \'%%" + username + "%%\'")
        
        db_conn.close()
        
        users = list(db_result)

        for user in users:
            if user.username == username and user.password == password:
                return user

        return None
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def create_user(email, username, password, firstname, lastname, gender, address, creditcard):
    if email is None or username is None or password is None or firstname is None:
        return False

    if lastname is None or gender is None or address is None or creditcard is None:
        return False

    if email_exists(email) or user_exists(username):
        return False

    try:
        db_conn = None
        db_conn = db_engine.connect()

        db_conn.execute(
            "INSERT INTO customers (email, username, password, firstname, lastname, gender, address1, creditcard) " +
            "VALUES (\'"+email+"\', \'"+username+"\', \'"+password+"\', \'"+firstname+"\', \'"+lastname+"\', \'"+gender+"\', \'"+address+"\', \'"+creditcard+"\')")
        
        db_conn.close()
        return True
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def load_cart(customer_id):
    if customer_id is None:
        return None

    try:
        db_conn = None
        db_conn = db_engine.connect()

        order = list(db_conn.execute('SELECT * FROM orders WHERE customer_id=\''+customer_id+'\' AND status IS NULL'))

        if len(order) == 0:
            db_conn.close()
            return None

        order = order[0]

        cart = list(db_conn.execute(
            'SELECT * FROM' +
            ' (SELECT prod_id, movieid, price, description FROM' +
            '  (SELECT prod_id, price, quantity FROM orderdetail WHERE orderid=\''+order.orderid+'\') AS od ' +
            '   JOIN products AS p ON od.prod_id=p.prod_id) AS prods' + 
            ' JOIN imdb_movies AS m ON prods.movieid = m.movieid'
        ))

        db_conn.close()
        return cart
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def load_movie(product_id):
    if product_id is None:
        return None

    try:
        db_conn = None
        db_conn = db_engine.connect()
        
        movie = list(db_conn.execute('SELECT * FROM products AS p JOIN imdb_movies AS m ON p.movieid=m.movieid WHERE p.prod_id=\''+product_id+'\''))

        db_conn.close()
        if len(movie) == 0:
            return None

        return movie[0]
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def add_to_cart(user, product_id):
    if user is None or product_id is None:
        return False

    try:
        db_conn = None
        db_conn = db_engine.connect()

        order = list(db_conn.execute('SELECT * FROM orders WHERE customer_id=\''+user.customerid+'\' AND status IS NULL'))

        if len(order) == 0:
            today = datetime.date.today()
            db_conn.execute(
                'INSERT INTO orders (customer_id, date, tax) ' +
                'VALUES (\''+user.customerid+'\', '+str(today)+'\', \'15\''
            )
            order = list(db_conn.execute('SELECT * FROM orders WHERE customer_id=\''+user.customerid+'\' AND status IS NULL'))

        order = order[0]

        order_detail = list(db_conn.execute('SELECT * FROM orderdetail WHERE orderid=\''+order.orderid+'\' AND prod_id=\''+product_id+'\''))

        if len(order_detail) == 0:
            db_conn.execute(
                'INSERT INTO orderdetail (orderid, prod_id, quantity) ' +
                'VALUES (\''+order.orderid+'\', \''+product_id+'\',\'1\')'
            )
        else:
            order_detail = order_detail[0]
            db_conn.execute('UPDATE orderdetail SET quantity=\''+(order_detail.quantity+1)+'\' WHERE orderid=\''+order_detail.orderid+'\' AND prod_id=\''+order_detail.prod_id+'\'')

        db_conn.close()
        return True
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def remove_from_cart(user, product_id):
    if user is None or product_id is None:
        return False

    try:
        db_conn = None
        db_conn = db_engine.connect()

        order = list(db_conn.execute('SELECT * FROM orders WHERE customer_id=\''+user.customerid+'\' AND status IS NULL'))

        if len(order) == 0:
            db_conn.close()
            return False

        order = order[0]

        order_detail = list(db_conn.execute('SELECT * FROM orderdetail WHERE order_id=\''+order.order_id+'\' AND prod_id=\''+product_id+'\''))

        if len(order_detail) == 0:
            db_conn.close()
            return False

        if order_detail.quantity == 1:
            db_conn.execute('DELETE FROM orderdetail WHERE order_id=\''+order.order_id+'\' AND prod_id=\''+product_id+'\'')
        else:
            db_conn.execute('UPDATE orderdetail SET quantity=\''+(order_detail.quantity-1)+'\' WHERE orderid=\''+order_detail.orderid+'\' AND prod_id=\''+order_detail.prod_id+'\'')
               
        db_conn.close() 
        return True
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
