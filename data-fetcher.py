import requests

i = 0

with open('db.txt', 'w') as fr:
    with open('movie-data.txt', 'r') as f:
        for line in f.readlines():
            line = line.split("*")
            if len(line) > 9:
                movie_id = line[3]
                date = line[9]
                title = line[10]

                r = requests.get(
                    f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=YOUR_API_KEY")
                t = requests.get(
                    f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY")
                runtime = t.json()
                json_data = r.json()

                cast = [cast['name'] for cast in json_data['cast']][0:2]
                director = [crew['name'] for crew in json_data['crew']
                            if 'director' in crew['job'].lower()]

                a = {date[0:4]}
                if len(director) != 0 and len(cast) > 1:
                    print(str(i / 10000 * 100)[0:3] + "%")
                    fr.write(
                        f"{title}*{date[0:4]}*{runtime['runtime']}*{cast[0]}*{cast[1]}*{director[0]}\n")
                    i += 1
