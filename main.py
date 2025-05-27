import requests


API_KEY = "263fc241"
#API_KEY = "mykey"
URL = "https://www.omdbapi.com"


def get_movie_data(title):
    payload = {"t": title, "apikey": API_KEY}
    movie_response = requests.get(URL, params=payload)
    movie_response = movie_response.json()

    return movie_response


title = input("Add name: ").strip()
movie_data = get_movie_data(title)
if movie_data:
    print(f"Title: {movie_data['Title']}")
    print(f"Year: {movie_data['Year']}")
    print(f"IMDB Rating: {movie_data['imdbRating']}")
    print(f"Director: {movie_data['Director']}")
    print(f"Actors: {movie_data['Actors']}")
    print(f"Poster: {movie_data['Poster']}")
