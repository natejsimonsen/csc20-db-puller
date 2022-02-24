import requests
import sys

j = 0
API_KEY = False

with open('.env') as f:
    API_KEY = f.readline().split('=')[1]

if not API_KEY:
    print("Must have a .env file with API_KEY=api_key")

def progress(count, total):
    percents = round(100.0 * count / float(total), 2)
    sys.stdout.write(f"\r{percents}%")
    sys.stdout.flush()


with open('db.txt', 'w') as f:
    for i in range(1, 501):
        r = requests.get(
            f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page={i}")
        credit_details = r.json()
        for result in credit_details['results']:
            j += 1
            progress(j, 10000)
            if 'id' in result and 'release_date' in result and 'title' in result:
                movie_id = result['id']
                date = result['release_date']
                title = result['title']

                r = requests.get(
                    f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}")
                t = requests.get(
                    f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}")
                movie_details = t.json()
                credit_details = r.json()
                runtime = movie_details['runtime']
                poster = movie_details['poster_path']

                if 'cast' in credit_details:
                    cast = [cast['name'] for cast in credit_details['cast']][0:2]
                    director = [crew['name'] for crew in credit_details['crew']
                                if 'director' == crew['job'].lower()]
                    a = {date[0:4]}
                    if len(director) != 0 and len(cast) > 1 and movie_id and date and title and runtime and poster:
                        f.write(
                            f"{title}*{date[0:4]}*{runtime}*{cast[0]}*{cast[1]}*{director[0]}*https://image.tmdb.org/t/p/w500{poster}\n")
