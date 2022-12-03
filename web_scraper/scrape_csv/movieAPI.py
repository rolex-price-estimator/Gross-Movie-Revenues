## Using MoviesDB API to grab movie information
## https://rapidapi.com/standingapi-standingapi-default/api/moviesdb5

import requests
import config
import json
import pandas as pd

url = "https://moviesdb5.p.rapidapi.com/om"

headers = {
	"X-RapidAPI-Key": config.api_key,
	"X-RapidAPI-Host": "moviesdb5.p.rapidapi.com"
}

# Following list would be the list of movie titles to search via the API
# Following is a sample
movieName = ['How the Grinch Stole Christmas', 'Mission: Impossible 2', 'Gladiator', 'The Perfect Storm', 'Meet the Parents', 'X-Men']

movieInfo = []
for i in movieName:
    querystring = {"t": i}  ## Replace the key with "s" to search for series and "i" to search by movie ID
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = json.loads(response.text)   # Loads response text into a dictionary type

    # Removing following keys
    remove_keys = ['Awards', 'Ratings', 'Metascore', 'imdbRating', 'imdbVotes', 'imdbID', 'Type', 'DVD', 'BoxOffice', 'Production', 'Website', 'Response']

    f_dict = dict([(key, val) for key, val in json_data.items() if key not in remove_keys])
    movieInfo.append(f_dict)

# Convert to df
# df = pd.DataFrame.from_dict(movieInfo)
# df.to_csv('moviesAPI.csv', index=False)