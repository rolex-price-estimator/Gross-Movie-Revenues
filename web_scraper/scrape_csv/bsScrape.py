import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import csv

URL = 'https://www.the-numbers.com/market/2022/top-grossing-movies'
req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

soup = bs(webpage, 'html.parser')
table = soup.find('table')
# rows = table.find_all("tr")

# for row in rows:
#     print(row.text.encode('iso-8859-1', errors='replace'))


# soup = bs(webpage, 'html.parser')
# table = soup.find('table')

# for movie in table.find_all('tr'):
#     title = movie.find('a')
#     print(title)


rows = table.find_all("tr")
movie_list = []
for row in rows:
    # print(row.text)
    movie_list.append(row.text.strip(" "))

# print(movie_list[2])


## Unable to save each movie as own row
with open('movies.csv', 'w', encoding='utf-8') as f:
    write = csv.writer(f)
    for item in movie_list:
        write.writerow([item.strip()])













# print(rows[1].text)
# print(table.prettify().encode('cp1252', errors='ignore'))
# rows = table.find_all('data')
# print(rows)





# titles = soup.find_all('td', class_ = 'data')
  
# print(titles)
# print(titles[0].text)

# for page in range(2000, 2022)[::-1]:

#     req = requests.get(f'https://www.the-numbers.com/market/{0}/top-grossing-movies'.format(page))
#     soup = bs(req.text, 'html.parser')

#     titles = soup.find_all('div', attrs={'class', 'data'})
#     print(titles)
    