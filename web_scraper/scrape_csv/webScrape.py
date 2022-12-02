from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import re
import csv
from divide_chunks import divide_chunks

URL = 'https://www.the-numbers.com/market/2022/top-grossing-movies'
req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = bs(webpage, 'html.parser')


movie_list = []
for tr in soup.find_all('tr'):
    for td in tr.find_all('td'):
        movie_list.append(td.get_text())

# print(movie_list)
print(len(movie_list))

full_lists = list(divide_chunks(movie_list, 7))
print(lists)


columns = ['Rank', 'Movie', 'Release Date', 'Distributor', 'Genre', '2022 Gross', 'Tickets Sold']

with open('movies.csv', 'w', encoding='utf-8') as f:
    write = csv.writer(f)
    write.writerow(columns)
    write.writerows(lists)
