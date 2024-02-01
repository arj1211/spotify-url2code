import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv('secrets.env')

# Get the Spotify Client ID and Client Secret from environment variables
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Get the access token
auth_response = requests.post(
    'https://accounts.spotify.com/api/token',
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    params={'grant_type': 'client_credentials', 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
)
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# Use the tracks endpoint
track_id = '5EFczt9dqrCu60udoD41Yy'
response = requests.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=headers)
response_data = response.json()['album']

track_name = response_data['name']
artist_names = [r['name'] for r in response_data['artists']]

print('Title:', track_name)
print('Artists:', artist_names)