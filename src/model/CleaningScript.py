import numpy as np
import pandas as pd
from datetime import datetime as dt
from sqlalchemy import create_engine

connection_url = 'postgresql+psycopg2://oahwyljl:sSrk8smQ16BCOVhHQBVWVtK2nVcCDmiF@peanut.db.elephantsql.com/oahwyljl'

try:
    # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
    engine = create_engine(connection_url)
    print( f"Connection created successfully.")
    
except Exception as ex:
    print("Connection could not be made due to the following error: \n", ex)

def replace_nan(x):
    x = x.replace('NaN', np.nan)
    x = x.replace('N/A', np.nan)
    return x

# Function to get minutes from format 'x min'
def get_minutes(x): 
    if pd.isna(x): 
        return np.nan 
    else: 
        try: 
            return int(x.split(' ')[0])
        except: 
            return np.nan

# Function for coding top director 
def has_top_director(x, director_list): 
    if pd.isna(x): 
        return np.nan 
    elif x in director_list: 
        return 1 
    else: 
        return 0 

# Function for converting column to list of actors instead of string 
def to_list(x): 
    if pd.isna(x): 
        return np.nan 
    else: 
        return x.split(', ')

# Function for coding top actors 
def has_top_actor(actors, actor_list): 
    # Check that the row is a list (it's NaN otherwise): 
    if isinstance(actors, list):
        for actor in actors:
            if actor in actor_list: 
                return 1 
        return 0 
    else: 
        return np.nan

# Function for coding ratings:  
# Decided to code missing data as 'Unrated' as well 
def recode_ratings(x): 
    # Check if the row is NaN: 
    if pd.isna(x): 
        return 'Unrated' 
    elif x in ['R', 'NC-17', 'X', 'TV-MA', 'MA-17']: 
        return 'R'
    elif x in ['PG-13', 'TV-14']: 
        return 'PG-13'
    elif x in ['PG', 'TV-PG']: 
        return 'PG'
    elif x in ['G', 'TV-G', 'TV-Y7']: 
        return 'G'
    elif x in ['Not Rated', 'Unrated', 'UNRATED']: 
        return 'Unrated'
    elif x in ['Approved', 'Passed']: 
        return 'Approved/Passed'
    else: 
        return np.nan 

# Function for recoding genre column: 
def has_genre(genres, genre_list): 
    # Check if the row is a list (NaN otherwise): 
    if isinstance(genres, list):
        for genre in genres:
            if genre in genre_list: 
                return 1 
        return 0 
    else: 
        return np.nan

# Function to clean API Data
def clean_APIdata(table_name):  #moviesinfo
    apidf = pd.read_sql_query(f"SELECT * from {table_name}", con=engine, parse_dates = ['released'])
    apidf.drop('movieinfo_id', axis=1, inplace=True)
    apidf = replace_nan(apidf)
    # apidf = apidf.replace('NaN', np.nan)
    # apidf = apidf.replace('N/A', np.nan)
    

    apidf = apidf.sort_values('year')
    apidf = apidf.reset_index(drop = True)
    apidf.drop_duplicates(subset = ['title', 'released'], inplace=True)    # Drop the duplicate rows based on title & release date
    apidf = apidf[apidf['seasons'].isna()]     # Drop rows where seasons > None
    apidf.drop('seasons', axis=1, inplace=True)
    apidf = apidf[apidf['year'].apply(lambda x: '–' not in x)]     # Drop rows without '-' in the year
    apidf = apidf.reset_index(drop = True)
    apidf['runtime'] = apidf['runtime'].apply(get_minutes)    # Convert runtime to minutes integer
    apidf['year'] = apidf['year'].apply(lambda x: int(x) if pd.notna(x) else np.nan)      # Recode year column to integer

    # Create the top directors columns
    top_10_directors = list(apidf['director'].value_counts()[0:10].index)
    top_50_directors = list(apidf['director'].value_counts()[0:50].index)
    top_100_directors = list(apidf['director'].value_counts()[0:100].index)
    apidf['top_10_dir'] = apidf['director'].apply(lambda x: has_top_director(x, top_10_directors))
    apidf['top_50_dir'] = apidf['director'].apply(lambda x: has_top_director(x, top_50_directors))
    apidf['top_100_dir'] = apidf['director'].apply(lambda x: has_top_director(x, top_100_directors))

    # Create top actors/writers columns
    apidf['actors'] = apidf['actors'].apply(to_list) 
    apidf['writer'] = apidf['writer'].apply(to_list)
    # Create a dictionary of actors to get the top actors by number of movies they've been in 
    actor_dict = {}
    for actors in apidf['actors']: 
        if isinstance(actors, list):
            for actor in actors: 
                actor_dict[actor] = actor_dict.get(actor, 0) + 1
    top_actors = sorted(actor_dict.items(), key=lambda item: item[1], reverse = True)
    # Movie cutoffs for top 10, top 50, and top 100 actors 
    cutoff_10_actors = top_actors[9][1]
    cutoff_50_actors = top_actors[49][1]
    cutoff_100_actors = top_actors[99][1]
    top_10_actors = [key for key, value in actor_dict.items() if value >= cutoff_10_actors]
    top_50_actors = [key for key, value in actor_dict.items() if value >= cutoff_50_actors]
    top_100_actors = [key for key, value in actor_dict.items() if value >= cutoff_100_actors]
    apidf['top_10_actors'] = apidf['actors'].apply(lambda x: has_top_actor(x, top_10_actors))
    apidf['top_50_actors'] = apidf['actors'].apply(lambda x: has_top_actor(x, top_50_actors))
    apidf['top_100_actors'] = apidf['actors'].apply(lambda x: has_top_actor(x, top_100_actors))

    # Encode Languge column
    languages = []
    for i in range(len(apidf['language'])):
        # account for null values 
        if pd.isna(apidf['language'][i]): 
            languages.append(np.nan)
        elif 'English' in apidf['language'][i].split(",") and (len(apidf['language'][i].split(",")) > 1):
            languages.append("English and others")
        elif 'English' in apidf['language'][i].split(",") and (len(apidf['language'][i].split(",")) == 1):
            languages.append("English only")
        else:
            languages.append('Foreign lang')
            
    apidf['language_coded'] = pd.DataFrame(languages)

    # Encode Country column
    countries = []
    for i in range(len(apidf['country'])):
        # account for null values 
        if pd.isna(apidf['country'][i]): 
            countries.append(np.nan)
        elif 'United States' in apidf['country'][i].split(",") and (len(apidf['country'][i].split(",")) > 1):
            countries.append("US and others")
        elif 'United States' in apidf['country'][i].split(",") and (len(apidf['country'][i].split(",")) == 1):
            countries.append("US only")
        else:
            countries.append('Foreign country')
    apidf['country_coded'] = pd.DataFrame(countries)

    # Encode rating column
    apidf['rating'] = apidf['rated'].apply(recode_ratings)

    # Encode genre column
    apidf['genre'] = apidf['genre'].apply(to_list) 
    # See what genres we have and how many of each: 
    genre_dict = {}
    for genres in apidf['genre']: 
        if isinstance(genres, list):
            for genre in genres: 
                genre_dict[genre] = genre_dict.get(genre, 0) + 1
    # Missing code for Short (173 movies) and Sport (255 movies)
    apidf['Action'] = apidf['genre'].apply(lambda x: has_genre(x, ['Action']))
    apidf['Adventure'] = apidf['genre'].apply(lambda x: has_genre(x, ['Adventure']))
    apidf['Fantasy/Sci-Fi'] = apidf['genre'].apply(lambda x: has_genre(x, ['Fantasy', 'Sci-Fi']))
    apidf['Crime'] = apidf['genre'].apply(lambda x: has_genre(x, ['Crime']))
    apidf['Thriller/Mystery'] = apidf['genre'].apply(lambda x: has_genre(x, ['Thriller', 'Mystery']))
    apidf['Drama'] = apidf['genre'].apply(lambda x: has_genre(x, ['Drama', 'Film-Noir', 'War', 'Western', 'Adult']))
    apidf['Horror'] = apidf['genre'].apply(lambda x: has_genre(x, ['Horror']))
    apidf['Comedy'] = apidf['genre'].apply(lambda x: has_genre(x, ['Comedy']))
    apidf['Documentary'] = apidf['genre'].apply(lambda x: has_genre(x, ['Documentary']))
    apidf['Family/Animated'] = apidf['genre'].apply(lambda x: has_genre(x, ['Family', 'Animation']))
    apidf['Biography/History'] = apidf['genre'].apply(lambda x: has_genre(x, ['Biography', 'History']))
    apidf['Romance'] = apidf['genre'].apply(lambda x: has_genre(x, ['Romance']))
    apidf['Music/Musical'] = apidf['genre'].apply(lambda x: has_genre(x, ['Musical', 'Music']))
    apidf['Likely TV'] = apidf['genre'].apply(lambda x: has_genre(x, ['News', 'Reality-TV', 'Talk-Show']))

    apidf['cut_title'] = apidf['title'].apply(lambda x: x[:27].lower())


    return apidf

# Function to clean scraped data
def scrape_data(table_name):    #moviesgross
    # Read data
    scrapedf = pd.read_sql_query(f"SELECT * from {table_name}", con=engine, parse_dates = ['release_date'])


    scrapedf.drop('moviegross_id', axis = 1, inplace=True)
    scrapedf = replace_nan(scrapedf)
    
    # scrapedf = scrapedf.replace('NaN', np.nan)
    # scrapedf = scrapedf.replace('N/A', np.nan)

    # Create dictionary with the first year (or 1st and 2nd) gross for every movie: 
    title_dict = {}
    for title in scrapedf['title']:
        # Only add title if it's not already in the dictionary: 
        if title not in title_dict: 
            # Check if the movie came out in December that year: 
            if list(scrapedf['release_date'][scrapedf['title'] == title].dt.month)[0] == 12: 
                # If so, add sum of first 2 gross entries to dictionary 
                sum_first_two_years = sum(list(scrapedf['gross'][scrapedf['title'] == title])[:2])
                title_dict[title] = sum_first_two_years
            else: 
                first_year_gross = list(scrapedf['gross'][scrapedf['title'] == title])[0]
                title_dict[title] = first_year_gross

    # Create the new column in scrapedf 
    scrapedf['1st_year_revenue'] = scrapedf['title'].apply(lambda x: title_dict[x])

    # Drop all duplicate movies from scrapedf, keeping only the first one by index: 
    scrapedf = scrapedf.drop_duplicates(subset=['title', 'release_date'], keep='first')

    scrapedf['cut_title'] = scrapedf['title'].apply(lambda x: x[:27].lower())

    return scrapedf

def join_df(table_name1, table_name2):
    apidf = clean_APIdata(table_name1)
    scrapedf = scrape_data(table_name2)

    df_final = scrapedf.merge(apidf, how='inner', left_on= ['cut_title', 'release_date'], \
                            right_on=['cut_title', 'released'], suffixes=["_rev", None])
    df_final = df_final[['1st_year_revenue', 'title', 'year', 'released', 'runtime', 'plot', 
        'top_10_dir', 'top_50_dir', 'top_100_dir', 'top_10_actors',
        'top_50_actors', 'top_100_actors', 'language_coded', 'country_coded',
        'rating', 'Action', 'Adventure', 'Fantasy/Sci-Fi', 'Crime',
        'Thriller/Mystery', 'Drama', 'Horror', 'Comedy', 'Documentary',
        'Family/Animated', 'Biography/History', 'Romance', 'Music/Musical',
        'Likely TV']]
    df_final.columns = ['1st_year_revenue', 'title', 'year', 'released', 'runtime', 'plot', 
       'top_10_dir', 'top_50_dir', 'top_100_dir', 'top_10_actors',
       'top_50_actors', 'top_100_actors', 'language', 'country',
       'rating', 'Action', 'Adventure', 'Fantasy/Sci-Fi', 'Crime',
       'Thriller/Mystery', 'Drama', 'Horror', 'Comedy', 'Documentary',
       'Family/Animated', 'Biography/History', 'Romance', 'Music/Musical',
       'Likely TV']        
    df_final = df_final.dropna()

    return df_final

print(clean_APIdata('moviesinfo').shape)
print(scrape_data('moviesgross').shape)    
print(join_df('moviesinfo','moviesgross').shape)     

