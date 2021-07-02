import requests 
import spotipy
import sqlalchemy
import os
import pandas as pd
from sqlalchemy import create_engine

def get_auth_response_data(auth_response):
  auth_response_data = auth_response.json()
  return auth_response_data

def status (auth_response):
  return auth_response.status_code

def requests_get_a1(artist_id, Base_URL, headers):
  r = requests.get(
                  Base_URL + 'artists/'
                  + artist_id + '/albums', headers = headers )
  data = r.json()
  return data
print ('data')
    
def requests_get_a2(artist_id_2, Base_URL, headers):
  r2 = requests.get(
                  Base_URL + 'artists/'
                  + artist_id_2 + '/albums', headers = headers )
  data_2 = r2.json()
  return data_2
    
def conv_dict_to_df(data):
  col_names = ['album name', 'release data']
  df = pd.DataFrame(columns = col_names)
  for album in data['items']:
    df.loc[len(df.index)] = [album ['name'], album ['release_date']]
  return df

def conv_dict_to_df_2(data_2):
  col_names = ['album name', 'release data']
  df = pd.DataFrame(columns = col_names)
  for album in data_2['items']:
    df.loc[len(df.index)] = [album ['name'], album ['release_date']]
  return df_2

def create_engine_obj():
  engine = create_engine('mysql://root:codio@localhost/Audio')
  return engine

def create_SQLTable(engine, df, df_2):
  df.to_sql('Slap_D', con=engine, if_exists='replace', index=False)
  df_2.to_sql('Natasha_Chansa', con=engine, if_exists='replace', index=False)
              
def save_database():
  return os.system("mysqldump -u root -pcodio database_name > file_name.sql")
              
def main():
  CLIENT_ID = '7d9c7a429a544319bcd98e0efa7b3104'
  CLIENT_SECRET = '1c5f121c38894affb3171ac0d724b828'
  BASE_URL = 'https://api.spotify.com/v1/'
  AUTH_URL = 'https://accounts.spotify.com/api/token'
  artist_id = '79EtBw4TQLmLrxGybCa8FK'
  artist_id_2 = '3pdp99HQonllwg9tEg7iAl'
  auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    })
  access_token = get_auth_response_data(auth_response)['access_token']

  headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
  }
  status(auth_response)
  data = requests_get_a1(artist_id, BASE_URL, headers)
  data_2 = requests_get_a2(artist_id_2, BASE_URL, headers)
  df = conv_dict_to_df(data)
  df_2 = conv_dict_to_df_2(data_2)
  engine = create_engine_obj()
  create_SQLTable(engine, df, df_2)
  save_database()
  
main()

#creating dataset from scratch
# df = pullDataFromAPIintoPandasDF()
# saveDatasetToFile(database_name, table_name, filenam cone, df)

# updating existing dataset
# df = loadDataset(database_name, table_name, filename, update=True)
# saveDatasetToFile(database_name, table_name, filename, df)

#load dataset and run analysis
df = loadDataset(database_name, table_name, filename)
#boxplot(df, 'Score')
highestScoringStories(df, 5)
  