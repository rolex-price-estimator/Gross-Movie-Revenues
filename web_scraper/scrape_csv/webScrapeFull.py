from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import re
import csv
from divide_chunks import divide_chunks

import sqlalchemy as db 
import psycopg2
from database_info.dbinformation import db_info
import pandas as pd

## Full scraper of the-numbers site capturing data from 2010-2021


def getMovies():

    for year in reversed(range(2000, 2022)):

        URL = f"https://www.the-numbers.com/market/{year}/top-grossing-movies".format(year)
        req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = bs(webpage, 'html.parser', from_encoding = 'utf-8')
        
        # list to store every row of data
        movie_list = []
        
        # grab data from table rows
        for tr in soup.find_all('tr'):
            for td in tr.find_all('td'):
                movie_list.append(td.get_text())
            movie_list.append(str(year))

        full_lists = list(divide_chunks(movie_list, 8))[:-1]    # Removes last row that contains the total amounts   

        for row in full_lists:
            # convert data to appropriate values
            row[0] = int(row[0])
            # remove $ and commas from gross revenue column
            row[6] = row[6].replace('$', '').replace(',', '')
            row[7] = row[7].replace(',', '')


        # column headers for adding data to CSV files
        columns = ['year', 'rank', 'title', 'release_date', 'distributor', 'genre', 'gross', 'tickets_sold']


        with open('moviesFull.csv', 'a', encoding = 'utf-8', newline='') as f:
            write = csv.writer(f)
            # if it's the first year in the data set, write the column headers to the csv
            if year == 2021:
                write.writerow(columns)
            write.writerows(full_lists)
             

        
    # print(compiled_data_set[0])
    loadAndInsertIntoDatabase()


def loadAndInsertIntoDatabase():
    url = f"{db_info['user']}:{db_info['pw']}@{db_info['url']}/{db_info['user']}"
    engine = db.create_engine('postgresql+psycopg2://' + url )      

    # read in csv file as pandas dataframe
    data = pd.read_csv('moviesFull.csv')
    df = pd.DataFrame(data)

    with engine.connect() as connection: 
        # iterate through each row in our data list
        try:
           
            for row in df.itertuples():

                # read in created csv_file and convert to dataframe, read in dataframe

                sql_stmt = """
                INSERT INTO moviesgross (year, rank, title, release_date, distributor, genre, gross, tickets_sold)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """

                # (?, ?, ?, ?, ?, ?, ?, ?)
                # VALUES (%s, %s, %s, %s, %s, %s, %s, %s);

                # store all elements in current row inside tuple for query parameter use
                # query_params = (el for el in row)
                #execute query
                connection.execute(sql_stmt, row.year, row.rank, row.title, row.release_date, row.distributor, row.genre, row.gross, row.tickets_sold)

        # handle any errors with communication to database
        except (Exception, psycopg2.Error) as err:
            print("Error while interacting with PostgreSQL...\n", err)

if __name__ == '__main__':
    getMovies()