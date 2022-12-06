## Using MoviesDB API to grab movie information
## https://rapidapi.com/standingapi-standingapi-default/api/moviesdb5

<<<<<<< HEAD
# import requests
# import config
# import json
# import pandas as pd
# import csv
# from tqdm import tqdm
=======
import requests
import config
import json
import pandas as pd
import csv
from tqdm import tqdm
>>>>>>> 500ad244c8c8b783b02c08a4a5ea5bf74eac9807

# url = "https://moviesdb5.p.rapidapi.com/om"

# headers = {
# 	"X-RapidAPI-Key": config.api_key,
# 	"X-RapidAPI-Host": "moviesdb5.p.rapidapi.com"
# }

# # Following list would be the list of movie titles to search via the API
# # Following is a sample

# path = 'MargaretMovies.csv'

# df = pd.read_csv(path)
# movieList = df['Movie'].values.tolist()

# movieName = movieList
# # print(movieName)

<<<<<<< HEAD
# movieInfo = []
# for i in tqdm(movieName):
#     querystring = {"t": i}  ## Replace the key with "s" to search for series and "i" to search by movie ID
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     json_data = json.loads(response.text)   # Loads response text into a dictionary type
=======
movieInfo = []
for i in tqdm(movieName):
    querystring = {"t": i}  ## Replace the key with "s" to search for series and "i" to search by movie ID
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = json.loads(response.text)   # Loads response text into a dictionary type
>>>>>>> 500ad244c8c8b783b02c08a4a5ea5bf74eac9807

#     # Removing following keys
#     remove_keys = ['Awards', 'Ratings', 'Metascore', 'imdbRating', 'imdbVotes', 'imdbID', 'Type', 'DVD', 'BoxOffice', 'Production', 'Website', 'Response']

#     f_dict = dict([(key, val) for key, val in json_data.items() if key not in remove_keys])
#     movieInfo.append(f_dict)

# # Convert to df
print(movieInfo)
# df = pd.DataFrame.from_dict(movieInfo)
# df.to_csv('M_Part.csv', index=False)

