import urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup
import json

def get_bends_by_name(name, country=None):
    http = urllib3.PoolManager()
    json_data= http.request('GET', "https://www.metal-archives.com/search/ajax-band-search/?field=name&query="+name).data
    bands = json.loads(json_data)["aaData"]
    print(bands)
    results =[]
    if len(bands) == 1:
        band = bands[0]
        band_html = BeautifulSoup(band[0], "html.parser")
        band[0] = band_html.find("a")
        band.append(band[0].get("href"))
        band[0] = band_html.text[:len(name)]
        band.insert(0, band[-1].split('/')[-1])
        results.append(band)
        return results

    for band in bands:
        band_html = BeautifulSoup(band[0], "html.parser")
        band[0] = band_html.find("a")
        band.append(band[0].get("href"))
        band[0] = band_html.text[:len(name)]
        band.insert(0, band[-1].split('/')[-1])
        if band[0].lower() == name.lower():
            if country is None:
                results.append(band)
            else:
                if country.lower() == band[2].lower():
                    results.append(band)


    if len(results) == 0 and country is not None:
        return get_bends_by_name(name)
    return results

def get_no_of_band_albums(id):
    http = urllib3.PoolManager()
    data = http.request("GET", "https://www.metal-archives.com/band/discography/id/"+str(id)+"/tab/all").data
    soup = BeautifulSoup(data, "html.parser")
    table = soup.find("table", {"class":"display discog"})
    tbody = table.find("tbody")
    trs = tbody.findAll("tr")
    return len(trs)

def get_band_genre_and_no_of_albums(name, country=None):
    bands = get_bends_by_name(name, country)
    print(len(bands))
    if len(bands) == 1:
        band_id, band_name, genre, country, url=bands[0]
        no_of_albums = get_no_of_band_albums(band_id)
        return genre, no_of_albums
    return None, None

if __name__=="__main__":
    print(get_band_genre_and_no_of_albums("jig%20ai"))
