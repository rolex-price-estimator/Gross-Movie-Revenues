from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import re
import csv
from divide_chunks import divide_chunks

import sqlalchemy as db 
import psycopg2
from database_info.dbinformation import db_info
import pandas as pd

def getMovies():
    ## Scraping The-Numbers website for upcoming releases
    URL = "https://www.the-numbers.com/movies/release-schedule"
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = bs(webpage, 'html.parser', from_encoding = 'utf-8')

    movie_list = []
    for tr in soup.find_all('tr'):
        for td in tr.find_all('td'):
            for b in soup.find_all('b'):
                # for a in soup.find_all('a'):
                movie_list.append(b.get_text())
            # movie_list.append(td.get_text())
    full_lists = list(divide_chunks(movie_list, 1))[1:-3]    # Removes last 3 rows and first row that contains extra info
    columns = ['Title']

    df = pd.DataFrame(full_lists, columns=columns)
    df.drop_duplicates(inplace=True)
    df = df.iloc[:-4]

    df.to_csv('upcoming.csv', index=False)
                

            
    # print(compiled_data_set[0])
    loadAndInsertIntoDatabase()


def loadAndInsertIntoDatabase():
    url = f"{db_info['user']}:{db_info['pw']}@{db_info['url']}/{db_info['user']}"
    engine = db.create_engine('postgresql+psycopg2://' + url )      

    # read in csv file as pandas dataframe
    data = pd.read_csv('upcoming.csv')
    df = pd.DataFrame(data)

    with engine.connect() as connection: 
        # iterate through each row in our data list
        try:
           
            for row in df.itertuples():

                # read in created csv_file and convert to dataframe, read in dataframe

                sql_stmt = """
                INSERT INTO movies2023 (title)
                VALUES (%s);
                """

                # (?, ?, ?, ?, ?, ?, ?, ?)
                # VALUES (%s, %s, %s, %s, %s, %s, %s, %s);

                # store all elements in current row inside tuple for query parameter use
                # query_params = (el for el in row)
                #execute query
                connection.execute(sql_stmt, row.title)

        # handle any errors with communication to database
        except (Exception, psycopg2.Error) as err:
            print("Error while interacting with PostgreSQL...\n", err)

if __name__ == '__main__':
    getMovies()