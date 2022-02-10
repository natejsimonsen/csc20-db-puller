import requests

with open('movie-data.txt', 'w') as f:
    for i in range(1, 501):
        r = requests.get(
            f"https://api.themoviedb.org/3/movie/popular?api_key=YOUR_API_KEY&language=en-US&page={i}")
        json_data = r.json()
        for result in json_data['results']:
            f.write("*".join([str(val) for val in result.values()]) + '\n')
        print(str(i // 5) + '%')
