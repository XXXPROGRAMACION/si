#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
import json
import os
import sys

""" @app.route('/')
@app.route('/index')
def index():
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('index.html', title = "Home", movies=catalogue['peliculas'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'username' in request.form:
        # aqui se deberia validar con fichero .dat del usuario
        if request.form['username'] == 'pp':
            session['usuario'] = request.form['username']
            session.modified=True
            # se puede usar request.referrer para volver a la pagina desde la que se hizo login
            return redirect(url_for('index'))
        else:
            # aqui se le puede pasar como argumento un mensaje de login invalido
            return render_template('login.html', title = "Sign In")
    else:
        # se puede guardar la pagina desde la que se invoca 
        session['url_origen']=request.referrer
        session.modified=True        
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print (request.referrer, file=sys.stderr)
        return render_template('login.html', title = "Sign In")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index')) """


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'query' in request.args:
        movies_data = open(os.path.join(app.root_path,'catalogue/movies.json'), encoding="utf-8").read()
        movies = json.loads(movies_data)['movies']
        search_result = []
        for movie in movies:
            if (request.args['query'] in movie['title'] or request.args['query'] in movie['original_title']) and request.args['category'] in movie['genres']:    
                movie["poster"] = "./static/media/posters/"+str(movie["id"])+".jpg"
                movie["poster_alt"] = movie["original_title"].replace(" ", "-").lower()
                search_result.append(movie)
        return render_template('search.html', search_result=search_result)

    return render_template('index.html')


@app.route('/movie-detail/<int:movie_id>')
def movie_detail(movie_id):
    movies_data = open(os.path.join(app.root_path,'catalogue/movies.json'), encoding="utf-8").read()
    movies = json.loads(movies_data)['movies']
    movie = next(filter(lambda x : x["id"] == movie_id, movies), None)
    movie["genres_string"] = ", ".join(movie["genres"])
    movie["genres_string"] = movie["genres_string"][0].upper()+movie["genres_string"][1:]
    poster = {}
    poster["url"] = "../static/media/posters/" + str(movie_id) + ".jpg"
    poster["alt"] = movie["original_title"].replace(" ", "-").lower()
    return render_template('movie-detail.html', movie=movie, poster=poster)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/shopping-history')
def shopping_history():
    return render_template('shopping-history.html')