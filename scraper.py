import urllib3
from bs4 import BeautifulSoup
import em_api

if __name__ == "__main__":
    http = urllib3.PoolManager()
    html = http.request('GET', "http://www.metaldays.net/Line_up").data
    soup = BeautifulSoup(html, 'html.parser')
    with open("bands.csv", "w") as f:
        f.write("Band,Country,MDGenre,MAGenre,noOfAlbums,ytVideo\n")

    all_as = soup.find_all("a", {'class': 'article regular'})+ soup.find_all("a", {'class': 'article large'})
    for a in all_as:
        html_band = http.request('GET', a.get('href')).data
        soup_band = BeautifulSoup(html_band, 'html.parser')
        band_and_genre = soup_band \
            .find("div", {"id": "page"}) \
            .find("div", {"class": "content_header overflow"}) \
            .find("div", {"class": "inner"})
        try:
            band_yt_video = soup_band.find("div", {"class": "content_video"}).find("iframe").get("src")
        except:
            band_yt_video = ""
        name = band_and_genre.h1.string
        country = band_and_genre.span.string.split("(")[1][:-1]
        genre = band_and_genre.span.string.split("(")[0][:-1]
        name = name.replace("Ö", "O")
        MAGenre, no_of_albums = em_api.get_band_genre_and_no_of_albums(name, country, genre)
        if MAGenre is None:
            MAGenre = ""
            no_of_albums = 0
            print("\nCORRECT ME")
            print(name)
            print(country)
        with open("bands.csv","a") as f:
            f.write("%s,%s,%s,%s,%d,%s\n" % (name, country, genre, MAGenre,no_of_albums,band_yt_video))

