import requests
from bs4 import BeautifulSoup

if __name__=="__main__":
    r = requests.get("https://www.metaldays.net/Line_up")
    bs = BeautifulSoup(r.text)
    days = ["sobota","nedelja","ponedeljek","torek","sreda","četrtek","petek"]
    with open("lineup.csv","w") as f:
        for i in range(7):
            f.write(days[i]+" "+str(20+i)+". 07.\n")
            print(str(20+i)+". 07.")
            day = bs.find("div", {"id": "day"+str(i)})
            main = day.find("div",{"class": "lineup_stage main_stage"})
            second = day.find_all("div",{"class": "lineup_stage second_stage"})
            third = None
            if len(second) == 1:
                third = second[0]
                second = None
            elif len(second) == 2:
                third = second[1]
                second = second[0]

            if main:
                bands = main.find_all("div", {"class": "band_lineup"})
                bands = bands[::-1]
                bands = [(band.find("span", {"class": "time"}).text, band.find("span", {"class": "title"}).text) for band in bands]
                f.write("main\n")
                [f.write(band[0]+","+band[1]+"\n") for band in bands]
                print("main:",bands)

            if second:
                bands = second.find_all("div", {"class": "band_lineup"})
                bands = bands[::-1]
                bands = [(band.find("span", {"class": "time"}).text, band.find("span", {"class": "title"}).text) for band in
                         bands]
                print("second:", bands)
                f.write("\nsecond\n")
                [f.write(band[0] + "," + band[1] + "\n") for band in bands]
                print("main:", bands)
            if third:
                bands = third.find_all("div", {"class": "band_lineup"})
                bands = bands[::-1]
                bands = [(band.find("span", {"class": "time"}).text if band.find("span", {"class": "time"}) else " ",band.find("span", {"class": "title"}).text) for
                         band in bands]
                if main:
                    f.write("\n")
                f.write("third\n")
                [f.write(band[0] + "," + band[1] + "\n") for band in bands]
                print("third:",bands)
            f.write("\n")
            #print("MAIN",main)
        #print("SECOND",second)
        #print("THIRD",third)