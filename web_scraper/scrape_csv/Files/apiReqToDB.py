import csv
import sqlalchemy as db 
import psycopg2
from database_info.dbinformation import db_info
import pandas as pd
import requests
import config
from tqdm import tqdm
import json


def apiRequest():
  url = "https://moviesdb5.p.rapidapi.com/om"

  headers = {
    "X-RapidAPI-Key": config.api_key,
    "X-RapidAPI-Host": "moviesdb5.p.rapidapi.com"
  }

  # Following list would be the list of movie titles to search via the API
  # Following is a sample

  # !!!!!!!!!!!!!!!!!!!!!!!!
  # change to your file path 
  path = 'Archive/RyanMovies.csv'

  df = pd.read_csv(path)
  movieList = df['Movie'].values.tolist()

  movieName = movieList
  # print(movieName)

  movieInfo = []
  for i in tqdm(movieName):
    querystring = {"t": i}  ## Replace the key with "s" to search for series and "i" to search by movie ID
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = json.loads(response.text)   # Loads response text into a dictionary type

    # Removing following keys
    remove_keys = ['Awards', 'Ratings', 'Metascore', 'imdbRating', 'imdbVotes', 'imdbID', 'Type', 'DVD', 'BoxOffice', 'Production', 'Website', 'Response']

    f_dict = dict([(key, val) for key, val in json_data.items() if key not in remove_keys])
    movieInfo.append(f_dict)

  # Convert to df
  df = pd.DataFrame.from_dict(movieInfo)
  
  # add datafram data to database table
  loadAndInsertIntoDatabase(df)

def loadAndInsertIntoDatabase(df):
    url = f"{db_info['user']}:{db_info['pw']}@{db_info['url']}/{db_info['user']}"
    engine = db.create_engine('postgresql+psycopg2://' + url )      



    with engine.connect() as connection: 
        # iterate through each row in our data list
        try:
           
          for row in df.itertuples():

              # read in created csv_file and convert to dataframe, read in dataframe

              sql_stmt = """
              INSERT INTO moviesinfo (title, year, rated, released, runtime, genre, director, writer, actors, plot, language, country, poster, seasons)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
              """

              #execute query
              connection.execute(sql_stmt, row.Title, row.Year, row.Rated, row.Released, row.Runtime, row.Genre,
                                  row.Director, row.Writer, row.Actors, row.Plot, row.Language, row.Country, row.Poster, row.totalSeasons)

        # handle any errors with communication to database
        except (Exception, psycopg2.Error) as err:
            print("Error while interacting with PostgreSQL...\n", err)

if __name__ == '__main__':
    apiRequest()