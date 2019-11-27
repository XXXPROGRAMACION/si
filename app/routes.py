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
    return render_template("index.html")


@app.route("/search")
def search():
    """ movies_data = open(os.path.join(app.root_path,"database/catalogue/movies.json"), encoding="utf-8").read()
    movies = json.loads(movies_data)["movies"]
    search_result = []
    
    for movie in movies:
        if movie_filter(movie, request.args.get("q"), request.args.get("genre")):
            search_result.append(movie_add_poster(movie))

    search_result.sort(key=lambda x: x["title"]) """

    search_result = database.search_product(request.args.get("q"))
    #search_result = database.latest_movies(10)
    return render_template("search-result-db.html", search_result=search_result)


@app.route("/latest-movies")
def latest_movies():
    """ movies_data = open(os.path.join(app.root_path,"database/catalogue/movies.json"), encoding="utf-8").read()
    movies = json.loads(movies_data)["movies"]
    latest_movies = movies[:4]

    for movie in latest_movies:
        movie_add_poster(movie) """

    latest_movies = database.latest_movies(4)

    return render_template("search-result-db.html", search_result=latest_movies)


@app.route("/product-detail/<int:product_id>")
def product_detail(product_id):
    return render_template("product-detail.html", product=database.load_product(product_id))


@app.route("/login", methods=["get"])
def login():
    return render_template("login.html")


@app.route("/login", methods=["post"])
def autenticate():
    user = database.login(request.form.get("username"), request.form.get("password"))
    if user is None:
        flash("Usuario o contraseña inválida", "error")
        return render_template("login.html")
    
    session["user"] = user
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
    users_shopping_histories_data = open(os.path.join(app.root_path,"database/users/users_shopping_histories.json"), encoding="utf-8").read()
    users_shopping_histories = json.loads(users_shopping_histories_data)["users_shopping_histories"]
    shopping_history_raw = users_shopping_histories[session["user"]["username"]]
    shopping_history = { "months": [] }

    last_date = ["0", "0", "0"]
    current_month = None
    for movie in shopping_history_raw:
        movie["movie_title"] = load_movie(movie["movie_id"])["title"]
        date = movie["date"].split("/")
        if date[1] != last_date[1] or date[2] != last_date[2]:
            month_id = date[1] + "-" + date[2]
            month_name = get_month_string(date[1], date[2])
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
    shopping_cart_movies = []
    for movie_id, units in session["cart"].items():
        movie = load_movie(movie_id)
        movie["units"] = units
        shopping_cart_movies.append(movie)
        total += movie["price"]*units

    total = round(total, 2)
    
    return render_template("shopping-cart.html", movies=shopping_cart_movies, total=total)


@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    """ if session.get("cart") is None:
        session["cart"] = {}
        session["cart_size"] = 0
    
    if session["cart"].get(movie_id) is None:
        session["cart"][movie_id] = 1
    else:
        session["cart"][movie_id] += 1

    session["cart_size"] += 1
    session.modified = True
    return redirect(url_for("shopping_cart")) """


@app.route("/remove-from-cart/<int:movie_id>")
def remove_from_cart(movie_id):
    if session.get("cart") is None or session["cart"].get(movie_id) is None:
        return redirect(url_for("shopping_cart"))

    session["cart"][movie_id] -= 1
    session["cart_size"] -= 1

    if session["cart"][movie_id] == 0:
        session["cart"].pop(movie_id, None)

    session.modified = True
    return redirect(url_for("shopping_cart"))


@app.route("/checkout")
def checkout():
    if session.get("user") is None or session.get("cart") is None:
        return redirect(url_for("shopping_cart"))
    
    total = 0
    shopping_cart_movies = []
    for movie_id in session["cart"]:
        movie = load_movie(movie_id)
        shopping_cart_movies.append(movie)
        total += movie["price"]

    process_payment(session.get("user")["username"], shopping_cart_movies, total)
    session.pop("cart", None)
    session.modified = True
    
    return redirect(url_for("shopping_history"))


@app.route('/list-of-movies')
def listOfMovies():
    movies_1949 = database.db_listOfMovies1949()
    return render_template('list_movies.html', title = "Movies from Postgres Database", movies_1949 = movies_1949)