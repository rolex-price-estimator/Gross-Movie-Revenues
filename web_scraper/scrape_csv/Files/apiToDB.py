import csv
import sqlalchemy as db 
import psycopg2
from database_info.dbinformation import db_info
import pandas as pd



def loadAndInsertIntoDatabase():
    url = f"{db_info['user']}:{db_info['pw']}@{db_info['url']}/{db_info['user']}"
    engine = db.create_engine('postgresql+psycopg2://' + url )      

    # read in all 3 data sets as a list
    dfs = loadInCSVFiles()

    with engine.connect() as connection: 
        # iterate through each row in our data list
        try:
           
          for df in dfs:

            for row in df.itertuples():

                # read in created csv_file and convert to dataframe, read in dataframe

                sql_stmt = """
                INSERT INTO movieinfo (title, year, rated, released, runtime, genre, director, writer, actors, plot, language, country, poster)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
 
                #execute query
                connection.execute(sql_stmt, row.Title, row.Year, row.Rated, row.Released, row.Runtime, row.Genre,
                                    row.Director, row.Writer, row.Actors, row.Plot, row.Language, row.Country, row.Poster)

        # handle any errors with communication to database
        except (Exception, psycopg2.Error) as err:
            print("Error while interacting with PostgreSQL...\n", err)


def loadInCSVFiles():
  data1 = pd.read_csv('KPart.csv')
  data2 = pd.read_csv('RPart.csv')


  # return a list of dataframes
  return [data1, data2]

if __name__ == '__main__':
    loadAndInsertIntoDatabase()