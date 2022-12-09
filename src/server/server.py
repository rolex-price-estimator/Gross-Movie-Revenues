from flask import Flask, request, render_template
from db_queries.movienames import getMovieNames
from model_prediction.predict import apiQuery

# declare a flap initialized to a Flask instance
app = Flask(__name__)

# initialize a cache to mitigate need for duplicate request when user returns to root endpoint
movieTitlesCache = []
nameAttributecache = []

# define an endpoint to return the main html form
@app.route('/', methods=['GET'])
def index():
  # query database for movie names to add to form options
  # if they aren't already stored in the cache and store in cache
  # if not movieTitlesCache:
  if not movieTitlesCache:
    movietitles, nameAttributes = getMovieNames()
    for title in movietitles:
      movieTitlesCache.append(title)
    for name in nameAttributes:
      nameAttributecache.append(name)

  # render_template looks for files within a 'templates' directory
  # accepts key-word arguments to render in html document
  return render_template("index.html", movie_titles = movieTitlesCache, movie_attributes = nameAttributecache)


# endpoint to make model predictions
@app.route('/predict', methods=['POST'])
def predict():
  print("Request Sent!")
  # store movie title in a variable to be called in API
  data = request.form.get("movie_titles")
  # check if the movie data has an underscore, meaning spaces were parsed to store in attribute
  if data.find('_') != -1:
    data_list = data.split('_')
    title = " ".join(data_list)
  else:
    title = data

  print("Title: ", title)
  print("char: ", title[-1])

  # make API request with current title and store predicted results
  prediction = apiQuery(title)

  print(prediction)

  return render_template("predicted.html", model_prediction = prediction, title = title)


if __name__ == '__main__':
  # run() method of Flask class runs the application
  # on the local development server.
  app.run()