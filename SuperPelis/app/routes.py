#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from app import database
from flask import render_template, request, url_for, redirect, session, flash
from app.utils import *
import json
import os
import sys


@app.route("/")
def index():            
    return render_template("index.html", genres=database.get_all_genres())


@app.route("/search")
def search():
    search_result = database.search_product(request.args.get("q"), request.args.get("genre"))
    return render_template("search-result-db.html", search_result=search_result)


@app.route("/latest-movies")
def latest_movies():
    latest_movies = database.latest_movies(4)

    return render_template("search-result-db.html", search_result=latest_movies)


@app.route("/product-detail/<int:product_id>")
def product_detail(product_id):
    genres = database.get_genres(product_id)
    string = ""
    for genre in genres:
        string = string+genre.name+", "

    product=database.load_product(product_id)
    product["genres"] = string[:-2]
    return render_template("product-detail.html", product=product)


@app.route("/login", methods=["get"])
def login():
    return render_template("login.html")


@app.route("/login", methods=["post"])
def autenticate():
    user = database.login(request.form.get("username"), request.form.get("password"))
    if user is None:
        flash("Usuario o contraseña inválida", "error")
        return render_template("login.html")
    
    if not database.save_products_into_cart(user, session.get("cart")):
        flash("Error al guardar los productos del carrito", "error")

    session["user"] = user
    session["cart"] = database.load_cart(user.user_id)
    if session["cart"] is None:
        session["cart"] = []
    session["cart_size"] = 0
    for product in session["cart"]:
        session["cart_size"] += product["quantity"]
    session.modified = True
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("cart", None)
    session.pop("cart_size", None)
    session.modified = True
    return redirect(url_for("index"))


@app.route("/register", methods=["get"])
def register():
    return render_template("register.html")


@app.route("/register", methods=["post"])
def submit_register():
    if database.email_exists(request.form.get("email")):
        flash("E-mail " + request.form.get("email") + " ya registrado", "error")
        return render_template("register.html")

    if database.user_exists(request.form.get("username")):
        flash("Nombre de usuario " + request.form.get("username") + " ya registrado", "error")
        return render_template("register.html")
        
    ret = database.create_user(
        request.form.get("email"),
        request.form.get("username"),
        request.form.get("password"),
        request.form.get("fullname"),
        request.form.get("lastname"),
        request.form.get("gender"),
        request.form.get("direction"),
        request.form.get("bank-account")
    )

    if not ret:
        flash("Error interno en el registro de los datos", "error")
        return render_template("register.html")

    flash("Usuario registrado correctamente", "success")
    return redirect(url_for("login"))


@app.route("/shopping-history")
def shopping_history():
    if session.get("user") is None:
        flash("No puedes ver el historial de compra sin haber iniciado sesión", "error")
        return(redirect(url_for("index")))


    shopping_history_raw = database.load_user_history(session["user"])
    shopping_history = { "months": [] }

    last_date = ["0", "0", "0"]
    current_month = None
    for movie in shopping_history_raw:
        date = str(movie["date"]).split("-")
        if date[1] != last_date[1] or date[0] != last_date[0]:
            month_id = date[1] + "-" + date[0]
            month_name = get_month_string(date[1], date[0])
            current_month = { "id": month_id, "name": month_name, "movies": [movie] }
            shopping_history["months"].append(current_month)
        else:
            current_month["movies"].append(movie)
        last_date = date

    return render_template("shopping-history.html", shopping_history=shopping_history)


@app.route("/shopping-cart")
def shopping_cart():
    if session.get("cart") is None:
        return render_template("shopping-cart.html")
    
    total = 0
    for product in session["cart"]:
        total += float(product['price'])*int(product['quantity'])

    total = round(total, 2)
    
    return render_template("shopping-cart.html", products=session["cart"], total=total)


@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    if session.get("cart") is None:
        session["cart"] = []
        session["cart_size"] = 0

    if session.get("user") is not None and not database.add_to_cart(session["user"], product_id):
        flash("Error al añadir el producto al carrito", "error")
        return redirect(url_for("shopping_cart"))

    found = False
    for product in session["cart"]:
        if product['product_id'] == product_id:
            found = True
            product['quantity'] += 1
            break

    if not found:
        session["cart"].append(database.load_movie(product_id))
    
    session["cart_size"] += 1
    session.modified = True
    return redirect(url_for("shopping_cart"))


@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    if session.get("cart") is None:
        session["cart"] = []
        session["cart_size"] = 0
        return redirect(url_for("shopping_cart"))

    found = False
    for product in session["cart"]:
        if product['product_id'] == product_id:
            found = True
            if not database.remove_from_cart(session["user"], product_id):
                flash("Error interno al eliminar el producto del carrito", "error")
                return redirect(url_for("shopping-cart"))
            if product['quantity'] == 1:
                session["cart"].remove(product)
            else:
                product['quantity'] -= 1
            session["cart_size"] -= 1
            break

    if not found:
        flash("Error al eliminar el producto del carrito", "error")

    session.modified = True
    return redirect(url_for("shopping_cart"))


@app.route("/checkout")
def checkout():
    if session.get("user") is None or session.get("cart") is None:
        return redirect(url_for("shopping_cart"))

    database.process_payment(session.get("user"))
    session.pop("cart", None)
    session["cart"] = []
    session["cart_size"] = 0
    session.modified = True

    flash("Pago procesado correctamente", "success")
    return redirect(url_for("shopping_history"))
