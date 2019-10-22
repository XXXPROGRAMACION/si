#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session, flash
from app.utils import *
import json
import os
import sys


@app.route('/')
def index():
    movies_data = open(os.path.join(app.root_path,'catalogue/movies.json'), encoding="utf-8").read()
    movies = json.loads(movies_data)['movies']
    search_result = []
    
    for movie in movies:
        if movie_filter(movie, request.args.get('q'), request.args.get('genre')):
            search_result.append(movie_add_poster(movie))
            
    return render_template('index.html', search_result=search_result)


@app.route('/movie-detail/<int:movie_id>')
def movie_detail(movie_id):
    return render_template('movie-detail.html', movie=load_movie(movie_id))


@app.route('/add-to-cart/<int:movie_id>')
def add_to_cart(movie_id):
    if session.get('cart') is None:
        session['cart'] = []
    
    session['cart'].append(movie_id)
    session.modified = True
    return redirect(url_for('shopping_cart'))


@app.route('/login', methods=['get'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['post'])
def autenticate():
    if not is_valid(request.form.get('username'), request.form.get('password')):
        flash('Usuario o contraseña inválida', 'error')
        return render_template('login.html')
    
    session['user'] = get_user(request.form.get('username'))
    session.modified = True
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('cart', None)
    session.modified = True
    return redirect(url_for('index'))


@app.route('/register', methods=['get'])
def register():
    return render_template('register.html')


@app.route('/register', methods=['post'])
def submit_register():
    if email_exists(request.form.get('email')):
        flash('E-mail ' + request.form.get('email') + ' ya registrado', 'error')
        return render_template('register.html')

    if user_exists(request.form.get('username')):
        flash('Nombre de usuario' + request.form.get('username') + ' ya registrado', 'error')
        return render_template('register.html')

    add_user(request)
    return redirect(url_for('login'))


@app.route('/shopping-history')
def shopping_history():
    return render_template('shopping-history.html')


@app.route('/shopping-cart')
def shopping_cart():
    if session.get('cart') is None:
        return render_template('shopping-cart.html')
    
    shopping_cart_movies = []
    for movie_id in session['cart']:
        shopping_cart_movies.append(load_movie(movie_id))
    
    return render_template('shopping-cart.html', movies=shopping_cart_movies)


@app.route('/remove-from-cart/<int:movie_id>')
def remove_from_cart(movie_id):
    if session.get('cart') is None:
        return redirect(url_for('shopping_cart'))

    session['cart'].remove(movie_id)
    session.modified = True
    return redirect(url_for('shopping_cart'))