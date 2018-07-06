import urllib3
from bs4 import BeautifulSoup
import xlwt
import json


def get_bands_and_gens():
    b_a_g = {}
    with open("bands.csv") as f:
        for l in f:
            line = l.split(",")
            name = line[0]
            genre = line[3]
            if genre == "":
                genre = line[2]
            b_a_g[name] = genre
    return b_a_g


class XlWriter:
    def __init__(self):
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet('Lineup')
        self.row = 0

    def save(self):
        self.wb.save("lineup.xls")

    def write_day(self, day, name_of_day):
        # day = main, second, third
        col = 0
        main, second, third = day

        # init
        col_init = 0
        self.ws.write(self.row, col_init, name_of_day)
        if main is not None:
            self.ws.write(self.row+1, col_init, "Main Stage")
            col_init+=4
        if second is not None:
            self.ws.write(self.row + 1, col_init, "Second Stage")
            col_init+=4

        self.ws.write(self.row + 1, col_init, "Third Stage")

        self.row+=2

        # bends
        biggest_row = self.row
        if main is not None:
            curr_row = self.row
            for band in main:
                for i in range(0, len(band)):
                    self.ws.write(curr_row, col+i, band[i])
                curr_row+=1
                if biggest_row < curr_row:
                    biggest_row = curr_row
            col += 4

        if second is not None:
            curr_row = self.row
            for band in second:
                for i in range(0, len(band)):
                    self.ws.write(curr_row, col + i, band[i])
                curr_row += 1
                if biggest_row < curr_row:
                    biggest_row = curr_row
            col += 4

        if third is not None:
            curr_row = self.row
            for band in third:
                for i in range(0, len(band)):
                    self.ws.write(curr_row, col + i, band[i])
                curr_row += 1
                if biggest_row < curr_row:
                    biggest_row = curr_row
            col += 4

        self.row = biggest_row+2





if __name__ == "__main__":
    bands_and_gens = get_bands_and_gens()
    http = urllib3.PoolManager()
    html = http.request('GET', "http://www.metaldays.net/Line_up").data
    soup = BeautifulSoup(html, 'html.parser')
    xl_writer = XlWriter()
    for i in range(0, 7):
        day_html = soup.find("div", {"id": "day" + str(i)})
        sec_and_third = day_html.find_all("div", {"class": "lineup_stage second_stage"})
        if len(sec_and_third) == 1:
            third_soup = sec_and_third[0]
            second_soup = None
        else:
            third_soup = sec_and_third[1]
            second_soup = sec_and_third[0]
        main_soup = day_html.find("div", {"class": "lineup_stage main_stage"})


        day_name = third_soup.find("div", {"class": "l-stage l-second"}).text.split("Newfor")[0]

        main = None
        if main_soup is not None:
            main = []
            tmp = main_soup.findAll("div",{"class": "band_lineup"})
            bands = tmp[::-1]
            for band in bands:
                edited_band = []
                edited_band.append(band.find("span",{"class":"time"}).text)
                edited_band.append(band.find("span",{"class":"title"}).text.replace("Ö", "O"))
                try:
                    edited_band.append(bands_and_gens[edited_band[1]])
                except:
                    print("Needs correction ",edited_band[1])
                edited_band.append("")
                main.append(edited_band)

        second = None
        if second_soup is not None:
            second = []
            tmp = second_soup.findAll("div", {"class": "band_lineup"})
            bands = tmp[::-1]
            for band in bands:
                edited_band = []
                edited_band.append(band.find("span", {"class": "time"}).text)
                edited_band.append(band.find("span", {"class": "title"}).text.replace("Ö", "O"))
                try:
                    edited_band.append(bands_and_gens[edited_band[1]])
                except:
                    print("Needs correction ",edited_band[1])
                edited_band.append("")
                second.append(edited_band)

        third = None
        if third_soup is not None:
            third = []
            tmp = third_soup.findAll("div", {"class": "band_lineup"})
            bands = tmp[::-1]
            for band in bands:
                edited_band = []
                edited_band.append(band.find("span", {"class": "time"}).text)
                edited_band.append(band.find("span", {"class": "title"}).text.replace("Ö", "O"))
                try:
                    edited_band.append(bands_and_gens[edited_band[1]])
                except:
                    print("Needs correction ",edited_band[1])
                edited_band.append("")
                third.append(edited_band)



        xl_writer.write_day((main,second,third),day_name)

    xl_writer.save()

