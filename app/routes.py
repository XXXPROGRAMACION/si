#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
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
    movies_data = open(os.path.join(app.root_path,'catalogue/movies.json'), encoding="utf-8").read()
    movies = json.loads(movies_data)['movies']
    movie = next(filter(lambda x : x["id"] == movie_id, movies), None)
    movie_add_poster(movie)
    movie_add_genres_string(movie)
    return render_template('movie-detail.html', movie=movie)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['get'])
def register():
    return render_template('register.html')

@app.route('/register', methods=['post'])
def submit_register():
    add_user(request)
    return render_template('login.html')

@app.route('/shopping-history')
def shopping_history():
    return render_template('shopping-history.html')