# Gross-Movie-Revenues


## 1. Data Sources

1. Link to pull top movie titles per year along with their gross revenue: https://www.the-numbers.com/market/2022/top-grossing-movies
- Web scraped each year's top # movies to create a dataset of movies
2. Link to the API used to gather movie information based on the above movie titles:  https://rapidapi.com/standingapi-standingapi-default/api/moviesdb5
- Ran API calls to pull in the information for the movies found via the top charts. Not all movies were able to be found due to generic titles

## 2. Access Data 
1. Data is stored in PostgreSQL database. Instance of database is hosted on ElephantSQL
   Request accest to URL to view tables and information inside them.
   The current database size is 13MB while the max database size is 20 MB
   
   Tables to use:
    - moviesinfo:  contains information on each movie from the MoviesDB API
    - movies2023:  contains movies that are coming out in 2023 - these movies are used for predicitve purposes from the client
    - moviesgross: contains the movie titles and their annual gross box office revenue
      - look out for duplicate titles as some films are released into box office multiple years

   Additional tables created that can be deleted to free up space:
    - movieinfo: has unformated data for movie information, use moviesinfo
    - test:      used to structure column sizes for moviesgross

## 3. List of Experiments Ran

Two Pipeline Model Setup files can be found under the model folder. "...Final to Serialize.ipynb" was the notebook used to create the serialized model.

1. Ran LinearRegression, Ridge, Lasso, RandomForestRegressor default models on the data.
2. Based on default models' performances, we moved onto selecting RandomForestRegressor as best model and did hyperparameter tuning via GridSearchCV. 
3. Model was serialized as pkl file but could not be pushed to GitHub as it exceeded 100 MB.

## 4. Todo items

1. Load server to EC2 instance.
2. Load models to S3 bucket.
3. Use Cron to schedule web scraping, API requests, and adding information to database
   - check for new movies on the-numbers.com that have been out for a specified duration (minimum 2 weeks) and add to database
4. If time allows, find another API or database to pull better data