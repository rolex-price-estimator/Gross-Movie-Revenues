from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import re
import csv
from divide_chunks import divide_chunks

## Full scraper of the-numbers site capturing data from 2010-2021

for year in reversed(range(2000, 2022)):
    URL = f"https://www.the-numbers.com/market/{year}/top-grossing-movies".format(year)
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = bs(webpage, 'html.parser', from_encoding = 'utf-8')
    movie_list = []
    for tr in soup.find_all('tr'):
        for td in tr.find_all('td'):
            movie_list.append(td.get_text())
        movie_list.append(str(year))
    full_lists = list(divide_chunks(movie_list, 8))[:-1]    # Removes last row that contains the total amounts
    gross_year = str(year) + ' Gross' 
    columns = ['Year', 'Rank', 'Movie', 'Release Date', 'Distributor', 'Genre', gross_year, 'Tickets Sold']

    with open('moviesFull.csv', 'a', encoding = 'utf-8', newline='') as f:
        write = csv.writer(f)
        write.writerow(columns)
        write.writerows(full_lists)