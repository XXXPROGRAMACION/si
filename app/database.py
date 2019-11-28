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
db_table_movies = Table('movies', db_meta, autoload=True, autoload_with=db_engine)


def latest_movies(amount):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        
        db_result = db_conn.execute(
            "SELECT * \
            FROM \
                movies AS m \
                JOIN products AS p \
                ON m.movie_id=p.movie_id \
            ORDER BY year DESC \
            LIMIT " + str(amount)
        )
        
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


def search_product(title, genre, amount=50):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        if title is None:
            if genre is None:
                db_result = db_conn.execute(
                    "SELECT * \
                    FROM \
                        movies AS m \
                        JOIN products AS p \
                        ON m.movie_id=p.movie_id \
                    LIMIT " + str(amount)
                )
            else:
                db_result = db_conn.execute(
                    "SELECT * \
                    FROM \
                        movies AS m \
                        JOIN products AS p \
                        ON m.movie_id=p.movie_id \
                        JOIN movie_genres AS mg \
                        ON mg.movieid=m.movie_id \
                        JOIN ( \
                            SELECT * \
                            FROM genres AS g \
                            WHERE g.name LIKE \'%%" + str(genre) + "%%\') AS gr \
                        ON gr.genre_id=mg.genre_id \
                    LIMIT " + str(amount)
                )
        else:
            if genre is not None:
                db_result = db_conn.execute(
                    "SELECT * \
                    FROM \
                        movies AS m \
                        JOIN products AS p \
                        ON m.movie_id=p.movie_id \
                        JOIN movie_genres AS mg \
                        ON mg.movieid=m.movie_id \
                        JOIN ( \
                            SELECT * \
                            FROM genres AS g \
                            WHERE g.name LIKE \'%%" + str(genre) + "%%\') AS gr \
                        ON gr.genre_id=mg.genre_id \
                    WHERE m.title LIKE \'%%" + title + "%%\'\
                    LIMIT " + str(amount)
                )
            else:  
                db_result = db_conn.execute(
                    "SELECT * \
                    FROM \
                        movies AS m \
                        JOIN products AS p \
                        ON m.movie_id=p.movie_id \
                    WHERE m.title LIKE \'%%" + title + "%%\'\
                    LIMIT " + str(amount)
                )
        
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

        db_result = db_conn.execute(
            "SELECT * \
            FROM \
                movies AS m \
                JOIN products AS p \
                ON m.movie_id=p.movie_id \
            WHERE p.product_id=" + str(product_id) + "\
            LIMIT 1"
        )
        
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

        db_result = db_conn.execute(
            "SELECT * \
            FROM users AS u \
            WHERE u.username LIKE \'%%" + username + "%%\' \
            LIMIT 1"
        )
        
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

        db_result = db_conn.execute(
            "SELECT * \
            FROM users AS u \
            WHERE u.email LIKE \'%%" + email + "%%\'\
            LIMIT 1"
        )
        
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

        db_result = db_conn.execute(
            "SELECT * \
            FROM users AS u \
            WHERE u.username LIKE \'%%" + username + "%%\'"
        )
        
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


def create_user(email, username, password, firstname, lastname, gender, address, bank_account):
    if email is None or username is None or password is None or firstname is None:
        return False

    if lastname is None or gender is None or address is None or bank_account is None:
        return False

    if email_exists(email) or user_exists(username):
        return False

    try:
        db_conn = None
        db_conn = db_engine.connect()

        db_conn.execute(
            "INSERT INTO users (\
                email,\
                username, \
                password, \
                firstname, \
                lastname, \
                gender, \
                address, \
                bank_account) " +
            "VALUES (\'"
                +str(email)+"\', \'"
                +str(username)+"\', \'"
                +str(password)+"\', \'"
                +str(firstname)+"\', \'"
                +str(lastname)+"\', \'"
                +str(gender)+"\', \'"
                +str(address)+"\', \'"
                +str(bank_account)+"\')"
        )
        
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

        order = list(db_conn.execute(
            'SELECT * \
            FROM orders AS o \
            WHERE \
                o.user_id=\''+str(customer_id)+'\' \
                AND \
                status IS NULL'
        ))

        if len(order) == 0:
            db_conn.close()
            return None

        order = order[0]

        cart = list(db_conn.execute(
            'SELECT * \
            FROM \
                (SELECT \
                    od.product_id, \
                    od.quantity, \
                    p.movie_id, \
                    p.price, \
                    p.description \
                FROM \
                    (SELECT \
                        o.product_id, \
                        o.price, \
                        o.quantity \
                    FROM orders_details AS o \
                    WHERE o.order_id=\''+str(order.order_id)+'\'\
                ) AS od \
                JOIN products AS p \
                ON od.product_id=p.product_id) AS prods \
            JOIN movies AS m \
            ON prods.movie_id = m.movie_id'
        ))

        db_conn.close()

        ret = []
        for prod in cart:
            aux = dict(prod.items())
            aux["quantity"] = int(aux["quantity"])
            ret.append(aux)

        return ret
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
        
        movie = list(db_conn.execute(
            'SELECT *, \'1\' AS quantity\
            FROM products AS p \
            JOIN movies AS m \
            ON p.movie_id=m.movie_id \
            WHERE p.product_id=\''+str(product_id)+'\''
        ))

        db_conn.close()
        if len(movie) == 0:
            return None

        ret = dict(movie[0].items())
        ret["quantity"] = int(ret["quantity"])
        return ret
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def get_genres(movie_id):
    if movie_id is None:
        return None

    try:
        db_conn = None
        db_conn = db_engine.connect()
        
        genres = list(db_conn.execute(
            'SELECT *\
            FROM movie_genres AS p \
            JOIN movies AS m \
            ON p.movie_id=m.movie_id \
            WHERE p.product_id=\''+str(product_id)+'\''
        ))

        db_conn.close()
        if len(movie) == 0:
            return None

        ret = dict(movie[0].items())
        ret["quantity"] = int(ret["quantity"])
        return ret
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def get_all_genres():
    try:
        db_conn = None
        db_conn = db_engine.connect()

        genres = list(db_conn.execute(
            'SELECT name \
            FROM genres'
        ))

        db_conn.close()
        return genres
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

        order = list(db_conn.execute(
            'SELECT * \
            FROM orders AS o \
            WHERE \
                o.user_id=\''+str(user.user_id)+'\' \
                AND \
                o.status IS NULL'
        ))

        if len(order) == 0:
            today = datetime.date.today()
            db_conn.execute(
                'INSERT INTO orders (user_id, date, tax) \
                VALUES (\''+str(user.user_id)+'\', \''+str(today)+'\', \'15\')'
            )
            order = list(db_conn.execute(
                'SELECT * \
                FROM orders AS o \
                WHERE \
                    o.user_id=\''+str(user.user_id)+'\' \
                    AND \
                    o.status IS NULL'
            ))

        order = order[0]

        order_detail = list(db_conn.execute(
            'SELECT * \
            FROM orders_details AS o \
            WHERE \
                o.order_id=\''+str(order.order_id)+'\' \
                AND \
                o.product_id=\''+str(product_id)+'\''
        ))

        if len(order_detail) == 0:
            db_conn.execute(
                'INSERT INTO orders_details (order_id, product_id, quantity) ' +
                'VALUES (\''+str(order.order_id)+'\', \''+str(product_id)+'\',\'1\')'
            )
        else:
            order_detail = order_detail[0]
            db_conn.execute(
                'UPDATE orders_details AS o \
                SET quantity=\''+str((order_detail.quantity+1))+'\' \
                WHERE \
                    o.order_id=\''+str(order_detail.order_id)+'\' \
                    AND \
                    o.product_id=\''+str(order_detail.product_id)+'\''
            )

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

        order = list(db_conn.execute(
            'SELECT * \
            FROM orders AS o \
            WHERE \
                o.user_id=\''+str(user.user_id)+'\' \
                AND \
                status IS NULL'
        ))

        if len(order) == 0:
            db_conn.close()
            return False

        order = order[0]

        order_detail = list(db_conn.execute(
            'SELECT * \
            FROM orders_details AS od \
            WHERE \
                od.order_id=\''+str(order.order_id)+'\' \
                AND \
                od.product_id=\''+str(product_id)+'\''
        ))

        if len(order_detail) == 0:
            db_conn.close()
            return False

        order_detail = order_detail[0]

        if order_detail.quantity == 1:
            db_conn.execute(
                'DELETE FROM orders_details \
                WHERE \
                    order_id=\''+str(order.order_id)+'\' \
                    AND \
                    product_id=\''+str(product_id)+'\''
            )
        else:
            db_conn.execute(
                'UPDATE orders_details AS od \
                SET quantity=\''+str((order_detail.quantity-1))+'\' \
                WHERE \
                    od.order_id=\''+str(order_detail.order_id)+'\' \
                    AND \
                    od.product_id=\''+str(order_detail.product_id)+'\''
            )
               
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


def process_payment(user):
    if user is None:
        return False

    try:
        db_conn = None
        db_conn = db_engine.connect()

        db_conn.execute(
            'UPDATE orders \
            SET status=\'Paid\' \
            WHERE \
                user_id=\''+str(user.user_id)+'\' \
                AND \
                status IS NULL'
        )
        
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


def load_user_history(user):
    if user is None:
        return None

    try:
        db_conn = None
        db_conn = db_engine.connect()

        result = db_conn.execute(
            'SELECT * \
            FROM \
                (SELECT * \
                FROM orders AS ord \
                WHERE \
                    ord.user_id=\''+str(user.user_id)+'\' \
                    AND \
                    ord.status IS NOT NULL) \
                AS o \
            JOIN orders_details AS od \
            ON o.order_id=od.order_id \
            JOIN products AS p \
            ON od.product_id=p.product_id \
            JOIN movies AS m \
            ON p.movie_id=m.movie_id \
            ORDER BY o.date DESC'
        )
        
        db_conn.close()

        ret = []
        for movie in result:
            ret.append(dict(movie.items()))

        return ret
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def save_products_into_cart(user, products):
    if user is None or products is None:
        return False

    for product in products:
        if not add_to_cart(user, product["product_id"]):
            return False

    return True
        
