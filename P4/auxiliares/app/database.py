# -*- coding: utf-8 -*-

import os
import sys, traceback, time

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False, execution_options={"autocommit":False})

def dbConnect():
    return db_engine.connect()

def dbCloseConnect(db_conn):
    db_conn.close()

def getListaCliMes(db_conn, mes, anio, iumbral, iintervalo, use_prepare, break0, niter):

    # DONE: implementar la consulta; asignar nombre 'cc' al contador resultante
    consulta = """
        SELECT COUNT(*) AS cc
        FROM (
            SELECT
                o.customerid AS customer_id,
                SUM(od.price*od.quantity) AS total_amount
            FROM
                orderdetail AS od
                JOIN orders AS o
                ON od.orderid=o.orderid
            WHERE
                EXTRACT(YEAR FROM o.orderdate)=%s
                AND EXTRACT(MONTH FROM o.orderdate)=%s
            GROUP BY o.customerid
            HAVING SUM(od.price*od.quantity)>%s
        ) AS filtered_customers
    """
    
    # DONE: ejecutar la consulta 
    # - mediante PREPARE, EXECUTE, DEALLOCATE si use_prepare es True
    # - mediante db_conn.execute() si es False

    # Array con resultados de la consulta para cada umbral
    dbr=[]

    if use_prepare:
        db_conn.execute("PREPARE listaClientesMesPlan AS " + (consulta % (str(anio), str(mes), "$1")))

    for ii in range(niter):
        if use_prepare:
            res = list(db_conn.execute("EXECUTE listaClientesMesPlan(%s)" % (iumbral)))[0]
        else:
            res = list(db_conn.execute(consulta % (str(anio), str(mes), str(iumbral))))[0]

        # Guardar resultado de la query
        dbr.append({
            "umbral": iumbral,
            "contador": res[0]
        })

        # DONE: si break0 es True, salir si contador resultante es cero
        if break0 and res['cc'] == 0:
            break
        
        # Actualizacion de umbral
        iumbral += iintervalo

    if use_prepare:
        db_conn.execute("DEALLOCATE listaClientesMesPlan")
        print('Con PREPARE')
    else:
        print('Sin PREPARE')

                
    return dbr

def getMovies(anio):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select movietitle from imdb_movies where year = '" + anio + "'"
    resultproxy=db_conn.execute(query)

    a = []
    for rowproxy in resultproxy:
        d={}
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d[tup[0]] = tup[1]
        a.append(d)
        
    resultproxy.close()  
    
    db_conn.close()  
    
    return a
    
def getCustomer(username, password):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select * from customers where username='" + username + "' and password='" + password + "'"
    res=db_conn.execute(query).first()
    
    db_conn.close()  

    if res is None:
        return None
    else:
        return {'firstname': res['firstname'], 'lastname': res['lastname']}
    
def delCustomer(customerid, bFallo, bSQL, duerme, bCommit):
    
    # Array de trazas a mostrar en la página
    dbr=[]

    consulta_eliminar_customers = """
        DELETE FROM customers AS c
        WHERE c.customerid=%s
    """

    consulta_eliminar_orders = """
        DELETE FROM orders AS o
        WHERE o.customerid=%s
    """

    consulta_eliminar_orderdetail = """
        DELETE FROM orderdetail AS od
        WHERE od.orderid IN (
            SELECT o.orderid
            FROM orders AS o
            WHERE o.customerid=%s
        )
    """
    
    if bSQL:
        db_conn = dbConnect()
    else:
        Session = sessionmaker(bind=db_engine)
        metaData = MetaData(bind=db_engine, reflect=True)
        Customers = metaData.tables['customers']
        Orders = metaData.tables['orders']
        OrderDetail = metaData.tables['orderdetail']

    # DONE: Ejecutar consultas de borrado
    # - ordenar consultas según se desee provocar un error (bFallo True) o no
    # - ejecutar commit intermedio si bCommit es True
    # - usar sentencias SQL ('BEGIN', 'COMMIT', ...) si bSQL es True
    # - suspender la ejecución 'duerme' segundos en el punto adecuado para forzar deadlock
    # - ir guardando trazas mediante dbr.append()

    try:
        if bSQL:
            db_conn.execute('BEGIN')
        else:
            session = Session()
        # DONE: ejecutar consultas
        if not bFallo:
            dbr.append('Se elimina orderdetail.')
            if bSQL:
                db_conn.execute(consulta_eliminar_orderdetail % (customerid))
            else:
                sq = session.query(Orders).filter(Orders.c.customerid==int(customerid)).subquery()
                session.query(OrderDetail).filter(OrderDetail.c.orderid.in_(sq)).delete()
            dbr.append('Se elimina orders.')
            if bSQL:
                db_conn.execute(consulta_eliminar_orders % (customerid))
            else:
                session.query(Orders).filter(Orders.c.customerid==int(customerid)).delete()
            if duerme > 0:
                time.sleep(duerme)
            dbr.append('Se elimina customers.')
            if bSQL:
                db_conn.execute(consulta_eliminar_customers % (customerid))
            else:
                session.query(Customers).filter(Customers.c.id==int(customerid)).delete()
        else:
            dbr.append('Se elimina orderdetail.')
            if bSQL:
                db_conn.execute(consulta_eliminar_orderdetail % (customerid))
            else:
                sq = session.query(Orders).filter(Orders.c.customerid==int(customerid)).subquery()
                session.query(OrderDetail).filter(OrderDetail.c.orderid.in_(sq)).delete()
            if bCommit:
                dbr.append('Se hace commit.')
                if bSQL:
                    db_conn.execute('COMMIT')
                    db_conn.execute('BEGIN')
                else:
                    session.commit()
                    session.begin()
            dbr.append('Se elimina customers.')
            if bSQL:
                db_conn.execute(consulta_eliminar_customers % (customerid))
            else:
                session.query(Customers).filter(Customers.c.id==int(customerid)).delete()
            dbr.append('Se elimina orders.')
            if bSQL:
                db_conn.execute(consulta_eliminar_orders % (customerid))
            else:
                session.query(Orders).filter(Orders.c.customerid==int(customerid)).delete()
    except Exception as e:
        print(e)
        # DONE: deshacer en caso de error
        dbr.append('Fallo en la eliminación. Se hace rollback.')
        if bSQL:
            db_conn.execute('ROLLBACK')
        else:
            session.rollback()
    else:
        # DONE: confirmar cambios si todo va bien
        dbr.append('Se hace commit.')
        if bSQL:
            db_conn.execute('COMMIT')
            dbCloseConnect(db_conn)
        else:
            session.commit()
            session.close()
        
    return dbr

