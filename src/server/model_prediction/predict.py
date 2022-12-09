import requests
import json
import model_prediction.config as config
import pandas as pd
# import serialized model

def apiQuery(title):
  url = "https://moviesdb5.p.rapidapi.com/om"

  headers = {
    "X-RapidAPI-Key": config.api_key,
    "X-RapidAPI-Host": "moviesdb5.p.rapidapi.com"
  }

  # list to store movie information from API
  movieData = []

  # query with "t" key for movies
  queryParams = {"t": title} 
  # make request to api and store in response
  response = requests.request("GET", url, headers=headers, params=queryParams)
  #
  data = json.loads(response.text)   

  # Removing following keys
  unused_keys = ['Awards', 'Ratings', 'Metascore', 'imdbRating', 'imdbVotes', 'imdbID', 'Type', 'DVD', 'BoxOffice', 'Production', 'Website', 'Response']

  dataDict = {key: val for key, val in data.items() if key not in unused_keys}
  movieData.append(dataDict)

  # Convert to df
  df = pd.DataFrame.from_dict(movieData)

  print("DF: ")
  print(df)

  return formatData(df)

# manipulate data to match model features for a row
def formatData(df):
  # format data here...
  print("IN HERE")
  return predict(df)

# return model prediction on row
def predict(row):
  # make model prediction here and return...
  print("ALSO IN HERE!")
  # return generic number for template rendering
  prediction = 1029384756

  # format prediction into human readable string
  # representanted in dollar format
  prediction = "{:,}".format(prediction)
  prediction = '$' + prediction

  return prediction
