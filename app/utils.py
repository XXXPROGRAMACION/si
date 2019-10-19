from app import app
import json
import os

def movie_filter(movie, q, genre):
    if q is not None and q not in movie['title'] and q not in movie['original_title']:
        return False

    if genre is not None and genre not in movie['genres']:
        return False

    return True

def movie_add_poster(movie):
    movie["poster"] = "../static/media/posters/"+str(movie["id"])+".jpg"
    movie["poster_alt"] = movie["original_title"].replace(" ", "-").lower()
    return movie

def movie_add_genres_string(movie):
    movie["genres_string"] = ", ".join(movie["genres"])
    movie["genres_string"] = movie["genres_string"][0].upper()+movie["genres_string"][1:]
    return movie

def add_user(request):
    file_data = open(os.path.join(app.root_path,'users/users.json'), 'r', encoding="utf-8").read()

    data = json.loads(file_data)

    data['users'].append({
        'email': request.form.get('email'),
        'username': request.form.get('username'),
        'password': request.form.get('password'),
        'fullname': request.form.get('fullname'),
        'lastname': request.form.get('lastname'),
        'gender': request.form.get('gender'),
        'direction': request.form.get('direction'),
        'bank-account': request.form.get('bank-account')
    })
    json.dump(data, open(os.path.join(app.root_path,'users/users.json'), 'w', encoding="utf-8"), indent=2)

def is_valid(username, password):
    file_data = open(os.path.join(app.root_path,'users/users.json'), 'r', encoding="utf-8").read()

    user_data = json.loads(file_data)['users']

    for user in user_data:
        if user['username'] == username and user['password'] == password:
            return True

    return False

def get_user(username):
    file_data = open(os.path.join(app.root_path,'users/users.json'), 'r', encoding="utf-8").read()

    user_data = json.loads(file_data)['users']

    for user in user_data:
        if user['username'] == username:
            return user

    return None
