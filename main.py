import urllib3
from bs4 import BeautifulSoup
import json

if __name__ == "__main__":
    http = urllib3.PoolManager()
    html = http.request('GET', "http://www.metaldays.net/Line_up").data
    soup = BeautifulSoup(html, 'html.parser')
    with open("bands.csv", "w") as f:
        f.write("Band,Country,MDGenre,MAGenre\n")

    for a in soup.find_all("a", {'class': 'article regular'}):
        html_band = http.request('GET', a.get('href')).data
        soup_band = BeautifulSoup(html_band, 'html.parser')
        band_and_genre = soup_band \
            .find("div", {"id": "page"}) \
            .find("div", {"class": "content_header overflow"}) \
            .find("div", {"class": "inner"})
        name = band_and_genre.h1.string
        country = band_and_genre.span.string.split("(")[1][:-1]
        genre = band_and_genre.span.string.split("(")[0][:-1]
        name = name.replace("Ö", "O")
        metal_archives_json = http.request("GET",
                                           "http://em.wemakesites.net/search/band_name/"
                                           + name.replace(" ","%20")
                                           + "?api_key=0719b560-a154-4a9c-bae8-31f05f5e72c9").data.decode("utf-8")

        array_bands = json.loads(metal_archives_json)['data']['search_results']
        correct_band = None

        if len(array_bands) == 1:
            correct_band = array_bands[0]
        else:
            for b in array_bands:
                if b["country"].lower() == country.lower():
                    correct_band = b
                    break

        if len(array_bands) == 0:
            MAGenre = ""
        elif correct_band is not None:
            MAGenre = correct_band['genre']
        else:
            print("\nCORRECT ME")
            print(country)
            print(array_bands)
            MAGenre = ""

        with open("bands.csv","a") as f:
            f.write("%s,%s,%s,%s\n" % (name, country, genre, MAGenre))

