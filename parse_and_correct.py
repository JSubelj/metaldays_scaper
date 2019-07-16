from dataclasses import dataclass


@dataclass
class Band:
    name: str
    time: str
    country: str
    genre: str
    description: str
    flags: str



def parse_csv(file_name):
    lineup = {}
    with open(file_name, "r") as f:
        for line in f:
            if line == "\n" or line.rstrip().lstrip() == ",":
                continue
            days = ["sobota", "nedelja", "ponedeljek", "torek", "sreda", "četrtek", "petek"]
            stages = ["main","second","third"]
            if line[-1] == "\n":
                line = line[:-1]
            if line.split(" ")[0] in days:
                # to je začetek dneva
                day_name = line.split(",")[0]
                lineup[day_name] = {}
                continue

            if line.split(",")[0] in stages:
                # to je začetek stagea
                current_stage = line.split(",")[0]
                lineup[day_name][current_stage] = {}
                continue
            #print(line)
            band = line.split(",")
            band = [attr.rstrip().lstrip() for attr in band]
            if band[-1] == "\n":
                band[-1] = ""
            while len(band) < 6:
                band.append("")
            for i, entry in enumerate(band):
                band[i] = entry.rstrip().lstrip()


            lineup[day_name][current_stage][band[1]] = Band(band[1],band[0],band[2],band[3],band[4],band[5])
    return lineup

def add_old_description_to_new_lineup(old: dict, new: dict):
    lineup = {}
    for name_day, stages in new.items():
        lineup[name_day] = {}
        for current_stage, bands in stages.items():
            lineup[name_day][current_stage] = {}
            for band_name, band in bands.items():
                try:
                    band_w_info = old[name_day][current_stage][band_name]
                except KeyError:
                    print("bwi")
                    print(name_day, current_stage, band_name)

                lineup[name_day][current_stage][band_name] = Band(band_name, band.time, band_w_info.country, band_w_info.genre, band_w_info.description, band_w_info.flags)


    return lineup

def return_csv_line(*args):
    ret = ""
    for arg in args:
        ret += arg+","
    ret+="\n"
    return ret

from datetime import datetime, timedelta
def export_new_to_csv(lineup):
    with open("latest_lineup.csv","w") as f:

        for name_day, stages in lineup.items():
            f.write(name_day+"\n")
            for current_stage, bands in stages.items():
                f.write(current_stage + "\n")
                bands = [bands[key] for key in bands.keys()]


                bands = sorted(bands, key=lambda b: datetime.strptime(b.time.split(" ")[0],"%H:%M") if int(b.time.split(":")[0]) != 0 else datetime.strptime(b.time.split(" ")[0],"%H:%M") + timedelta(days=1) )


                for band in bands:
                    f.write(return_csv_line(band.time, band.name, band.country,band.genre, band.description, band.flags))
                f.write("\n")




if __name__=="__main__":
    org = parse_csv("lineup_org.csv")
    new = parse_csv("lineup.csv")
    #print(new)
    #add_old_description_to_new_lineup(org, new)
    new_corrected = add_old_description_to_new_lineup(org,new)
    export_new_to_csv(new_corrected)