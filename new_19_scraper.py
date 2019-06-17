import requests
from bs4 import BeautifulSoup

if __name__=="__main__":
    r = requests.get("https://www.metaldays.net/Line_up")
    print(r.text)