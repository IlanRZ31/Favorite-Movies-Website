import requests
movie_url = "https://api.themoviedb.org/3/search/movie"
movie_details_url = "https://api.themoviedb.org/3/movie/359724"

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYTIzNTY0YWFhYmI5MjM5MzdhMzg1YzllMjA4YTgzMCIsInN1YiI6IjY0YjcxNmJhYjUxM2E4MDEyYzI1NmZmMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Z6GHTcsfUiBFuFti9BU8Kma4Ru3Ezr_k-to5SdCYaNg"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYTIzNTY0YWFhYmI5MjM5MzdhMzg1YzllMjA4YTgzMCIsInN1YiI6IjY0YjcxNmJhYjUxM2E4MDEyYzI1NmZmMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Z6GHTcsfUiBFuFti9BU8Kma4Ru3Ezr_k-to5SdCYaNg"
}
parameters = {"movie_id": 359724}
response = requests.get(movie_details_url, headers=headers, params=parameters)
data = response.json()
print(data)

parameters = {"query": "ford v ferrari"}
response = requests.get(movie_url, headers=headers, params=parameters)
data = response.json()["results"]
print(data)

