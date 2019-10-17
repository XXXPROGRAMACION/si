def movie_filter(movie, q, genre):
    if q is not None and q not in movie['title'] and q not in movie['original_title']:
        return False

    if genre is not None and genre not in movie['genres']:
        return False

    return True

def movie_add_poster(movie):
    movie["poster"] = "./static/media/posters/"+str(movie["id"])+".jpg"
    movie["poster_alt"] = movie["original_title"].replace(" ", "-").lower()
    return movie

def movie_add_genres_string(movie):
    movie["genres_string"] = ", ".join(movie["genres"])
    movie["genres_string"] = movie["genres_string"][0].upper()+movie["genres_string"][1:]
    return movie