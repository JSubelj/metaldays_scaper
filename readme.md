# Metaldays scraper and lineup maker
## Scraper
I created a simple Metaldays scraper (scraper.py) that scrapes info (genre, yt link) from metaldays.net. It also queries metal-archives.com for data about genre (we all know that Metaldays isn't really good at classifying  genres) and no. of albums (this includes singles etc). It then stores information inside a bands.csv file which can be opened by Excel and then stored as .xls file. 
## Lineup maker
I also created a script (lineup_editor.py) that polls data from Metaldays web page, when bands are playing. It then stores it inside lineup.xls, which also includes data about genres and an empty cell for comments.

## How to run
If you wanna run my code u need urllib3, beautiful soup, json and xlwt moduls. You first need to run scraper.py because lineup_editor.py depends on bands.csv file. 

# Disclaimer
I created this two programs so I don't have to do this stuff by hands. If I'll have some free time I will try to clean up and speed up the code and make it more professional looking with pip requirements etc. Code is ofc opensource and pull request are very welcome. If you like programs or the bands.csv and lineup.xls you can always find me on Metaldays and buy me a beer :D. If you would like to contact me w suggestions or anything here's my email: jan.subelj010@gmail.com





