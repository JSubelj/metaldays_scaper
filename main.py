import urllib3
from bs4 import BeautifulSoup
import json

API_KEY="4fa44a95-35f9-4a13-97f8-7f306cb96903"

if __name__ == "__main__":
    http = urllib3.PoolManager()
    html = http.request('GET', "http://www.metaldays.net/Line_up").data
    soup = BeautifulSoup(html, 'html.parser')
    with open("bands.csv", "w") as f:
        f.write("Band,Country,MDGenre,MAGenre,noOfAlbums,ytVideo\n")

    for a in soup.find_all("a", {'class': 'article regular'}):
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
        metal_archives_json = http.request("GET",
                                           "http://em.wemakesites.net/search/band_name/"
                                           + name.replace(" ","%20")
                                           + "?api_key="+API_KEY).data.decode("utf-8")


        array_bands = json.loads(metal_archives_json)['data']['search_results']
        correct_band = None

        if len(array_bands) == 1:
            correct_band = array_bands[0]
        else:
            for b in array_bands:
                if b["country"].lower() == country.lower():
                    correct_band = b
                    break

        no_of_albums = 0
        if len(array_bands) == 0:
            MAGenre = ""
        elif correct_band is not None:
            MAGenre = correct_band['genre']
            metal_archives_json = http.request("GET",
                                               "http://em.wemakesites.net/band/"
                                               + correct_band['id']
                                               + "?api_key=" + API_KEY).data.decode("utf-8")

            band_discography = json.loads(metal_archives_json)['data']["discography"]

            json.loads(metal_archives_json)['data'].keys()
            for album in band_discography:
                if album['type'].lower() == "Full-length".lower():
                    no_of_albums +=1
            #print(correct_band['name'])
            #print(no_of_albums)
        else:
            print("\nCORRECT ME")
            print(country)
            print(array_bands)
            MAGenre = ""

        with open("bands.csv","a") as f:
            f.write("%s,%s,%s,%s,%d,%s\n" % (name, country, genre, MAGenre,no_of_albums,band_yt_video))

