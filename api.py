import requests
import pandas as pd
import spotipy
import sqlalchemy
from sqlalchemy import create_engine

CLIENT_ID = '7d9c7a429a544319bcd98e0efa7b3104'
CLIENT_SECRET = '1c5f121c38894affb3171ac0d724b828'

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
#Test 1 validate client id and cient secret
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

#  convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

#Test 2 Check if track id is valid
# Track ID from the URI
track_id = '6y0igZArWVi6Iz0rj35c1Y'

#Test 3 Verify the response is not empty
#Test 4 Validate json format is correct
# actual GET request with proper header
r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
r = r.json()
print(r)
loudness = r['loudness']
energy = r['energy']
key = r['key']

col_names = ['Loudness', 'Energy', 'Key']
df = pd.DataFrame(columns = col_names)
df.loc[len(df.index)] = [loudness, energy, key]
print(df)

engine = create_engine('mysql://root:codio@localhost/Audio')
df.to_sql('Audio_Features', con=engine, if_exists='replace', index=False)
