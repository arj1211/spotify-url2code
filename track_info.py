import os
from dotenv import load_dotenv
import requests

class SpotifyAPI:
    def __init__(self, client_id:str, client_secret:str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        auth_response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            params={'grant_type': 'client_credentials', 'client_id': self.client_id, 'client_secret': self.client_secret}
        )
        auth_response_data = auth_response.json()
        return auth_response_data['access_token']

    def get_track_info(self, track_id:str):
        headers = {
            'Authorization': 'Bearer {token}'.format(token=self.access_token)
        }
        response = requests.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=headers)
        response_data = response.json()['album']

        track_name = response_data['name']
        artist_names = [r['name'] for r in response_data['artists']]

        return track_name, artist_names

if __name__ == "__main__":
    load_dotenv('secrets.env')
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

    spotify = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)
    track_name, artist_names = spotify.get_track_info('5EFczt9dqrCu60udoD41Yy')

    print('Title:', track_name)
    print('Artists:', artist_names)
