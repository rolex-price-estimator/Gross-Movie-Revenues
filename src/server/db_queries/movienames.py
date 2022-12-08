from db_queries.database_info.dbinformation import db_info
import sqlalchemy as db 
import psycopg2


def getMovieNames():
  url = f"{db_info['user']}:{db_info['pw']}@{db_info['url']}/{db_info['user']}"
  engine = db.create_engine('postgresql+psycopg2://' + url )      



  with engine.connect() as connection: 
    # iterate through each row in our data list
    try:
      # read in created csv_file and convert to dataframe, read in dataframe

      sql_stmt = """
      SELECT DISTINCT title
      FROM moviesinfo
      LIMIT 200;
      """

      #execute query
      results = connection.execute(sql_stmt).fetchall()
      
      # remove tuple from results and sort alphabteically, ascending
      titles = sorted([val[0] for val in results])
      # create list for attribute names
      # needs _ to be assigned to <option> tag 'value' attribute to send to server during form request
      attributes = [convertTitle(val) for val in titles]
      
      
     
  
      print('Titles: ', titles[:5])
      print('Attributes: ', attributes[:5])
      return titles, attributes
  # handle any errors with communication to database
    except (Exception, psycopg2.Error) as err:
      print("Error while interacting with PostgreSQL...\n", err)
      return []
  # return the results to endpoint function
  

def convertTitle(title):
  temp = title.split()
  if len(temp) > 1:
    return '_'.join(temp)
  return temp[0]
