from bs4 import BeautifulSoup
import requests
import json

result_dict = dict()

try:
    source = requests.get("https://www.imdb.com/chart/top", headers={'User-Agent': 'Mozilla/5.0'})
    source.raise_for_status()
    soup = BeautifulSoup(source.text, features="html.parser")
    movies = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-3a353071-0 wTPeg compact-list-view ipc-metadata-list--base").find_all('li')
    for rank,movie in enumerate(movies):
        movie_name = movie.find('div', class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-14dd939d-7 fjdYTb cli-title").a.text
        movie_name = movie_name.split('.')[1].strip()
        rating = movie.find('span', class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating").text
        year_and_duration = movie.find('div', class_="sc-14dd939d-5 cPiUKY cli-title-metadata").find_all('span',class_="sc-14dd939d-6 kHVqMR cli-title-metadata-item")
        year = year_and_duration[0].text
        duration = year_and_duration[1].text
        result_dict[rank+1] = {
            "name": movie_name,
            "rating": rating,
            "year": year,
            "duration": duration,
        }
    with open("results.json","w") as obj:
        obj.write(json.dumps(result_dict, indent=4))
except Exception as e:
    print(e)