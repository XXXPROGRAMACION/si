from app import app
import json
import os
from datetime import date


def movie_filter(movie, q, genre):
    q = q.lower()

    if q is not None and q not in movie["title"].lower() and q not in movie["original_title"].lower():
        return False

    if genre is not None and len(genre) is not 0 and genre not in movie["genres"]:
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


def load_movie(movie_id):
    movies_data = open(os.path.join(app.root_path,"database/catalogue/movies.json"), encoding="utf-8").read()
    movies = json.loads(movies_data)["movies"]
    movie = next(filter(lambda x : x["id"] == movie_id, movies), None)
    movie_add_poster(movie)
    movie_add_genres_string(movie)

    return movie


def add_user(request):
    file_data = open(os.path.join(app.root_path,"database/users/users.json"), "r", encoding="utf-8").read()

    data = json.loads(file_data)

    data["users"].append({
        "email": request.form.get("email"),
        "username": request.form.get("username"),
        "password": request.form.get("password"),
        "fullname": request.form.get("fullname"),
        "lastname": request.form.get("lastname"),
        "gender": request.form.get("gender"),
        "direction": request.form.get("direction"),
        "bank-account": request.form.get("bank-account")
    })
    
    json.dump(data, open(os.path.join(app.root_path,"database/users/users.json"), "w", encoding="utf-8"), indent=2)


def is_valid(username, password):
    file_data = open(os.path.join(app.root_path,"database/users/users.json"), "r", encoding="utf-8").read()

    user_data = json.loads(file_data)["users"]

    for user in user_data:
        if user["username"] == username and user["password"] == password:
            return True

    return False


def get_user(username):
    file_data = open(os.path.join(app.root_path,"database/users/users.json"), "r", encoding="utf-8").read()

    user_data = json.loads(file_data)["users"]

    for user in user_data:
        if user["username"] == username:
            return user

    return None


def user_exists(username):
    file_data = open(os.path.join(app.root_path,"database/users/users.json"), "r", encoding="utf-8").read()

    user_data = json.loads(file_data)["users"]

    for user in user_data:
        if user["username"] == username:
            return True

    return False


def email_exists(email):
    file_data = open(os.path.join(app.root_path,"database/users/users.json"), "r", encoding="utf-8").read()

    user_data = json.loads(file_data)["users"]

    for user in user_data:
        if user["email"] == email:
            return True

    return False


def process_payment(username, movies, total):
    file_data = open(os.path.join(app.root_path,"database/users/users_shopping_histories.json"), "r", encoding="utf-8").read()

    data = json.loads(file_data)

    today = date.today()
    # dd/mm/YY
    date_str = today.strftime("%d/%m/%Y")

    if data["users_shopping_histories"].get(username) is None:
        data["users_shopping_histories"][username] = []

    for movie in movies:
        data["users_shopping_histories"][username].insert(0, {
            "movie_id": movie["id"],
            "date": date_str,
            "price": movie["price"]
        })
    
    json.dump(data, open(os.path.join(app.root_path,"database/users/users_shopping_histories.json"), "w", encoding="utf-8"), indent=2)

