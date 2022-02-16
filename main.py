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
        json_data = r.json()
        for result in json_data['results']:
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
                runtime = t.json()['runtime']
                json_data = r.json()

                if 'cast' in json_data:
                    cast = [cast['name'] for cast in json_data['cast']][0:2]
                    director = [crew['name'] for crew in json_data['crew']
                                if 'director' == crew['job'].lower()]
                    a = {date[0:4]}
                    if len(director) != 0 and len(cast) > 1 and movie_id and date and title and runtime:
                        f.write(
                            f"{title}*{date[0:4]}*{runtime}*{cast[0]}*{cast[1]}*{director[0]}\n")
