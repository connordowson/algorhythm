import requests
import json
import urllib
import webbrowser
import base64
from datetime import datetime

from .models import Song, User

def make_authorization_headers(client_id, client_secret):
    auth_header = base64.b64encode((client_id + ':' + client_secret).encode('ascii'))
    return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

class SpotifyWrapper(object):

    AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, redirect_uri, scope):

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.code = None


    def get_authorize_url(self):

        queries = {'client_id': self.client_id, 'redirect_uri': self.redirect_uri, 'scope': self.scope, 'response_type': 'code', 'show_dialog:' : 'true'}

        urlparams = urllib.parse.urlencode(queries)

        url = "%s?%s" % (self.AUTHORIZE_URL, urlparams)

        return(url)


    def get_authorize_token(self, code):

        headers = make_authorization_headers(self.client_id, self.client_secret)

        queries = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': self.redirect_uri}

        response = requests.post(self.TOKEN_URL, data = queries, headers = headers)

        token_info = response.json()

        return(token_info['access_token'])


    def get_top_tracks(self, token, time_range):

        endpoint = 'https://api.spotify.com/v1/me/top/tracks'

        queries = {'time_range': time_range, 'limit': 50}

        urlparams = urllib.parse.urlencode(queries)

        url = "%s?%s" % (endpoint, urlparams)

        headers = {'Authorization': 'Bearer {0}'.format(token), 'Accept': 'application/json', 'Content-Type' : 'application/json'}

        results = requests.get(url, headers = headers)

        results = results.json()

        tracks_list = []

        top_tracks = results['items']

        for index, track in enumerate(top_tracks):

            # Check if song info is already on the database
            if not Song.objects.filter(song_id = track['id']).exists():

                track_info = {}
                track_info['song_id'] = track['id']
                track_info['title'] = track['name']
                track_info['artist'] = track['artists'][0]['name']
                track_info['album'] = track['album']['name']
                track_info['image_url'] = track['album']['images'][0]['url']

                release_date_precision = track['album']['release_date_precision']

                if(release_date_precision == "year"):
                    track_info['release_date'] = int(track['album']['release_date'])
                else:               
                    formatted_date = datetime.strptime(track['album']['release_date'], '%Y-%m-%d')
                    year = formatted_date.year
                    track_info['release_date'] = int(year)

                # Get audio features for users top songs
                results = self.get_audio_features(track['id'], token)

                track_info['audio_features'] = results

                # Add list of tracks to variable to be used in context
                tracks_list.append(track_info)
            else:
                this_song = Song.objects.get(song_id = track['id'])
                track_info = {}
                track_info['song_id'] = getattr(this_song, 'song_id')
                track_info['title'] = getattr(this_song, 'title')
                track_info['artist'] = getattr(this_song, 'artist')
                tracks_list.append(track_info)

        return tracks_list

    def get_audio_features(self, song_id, token):

        endpoint = 'https://api.spotify.com/v1/audio-features/'

        queries = {'id': song_id}

        urlparams = urllib.parse.urlencode(queries)

        url = "%s?%s" % (endpoint, urlparams)

        headers = {'Authorization': 'Bearer {0}'.format(token), 'Accept': 'application/json', 'Content-Type' : 'application/json'}

        results = requests.get(url, headers = headers)

        return(results.json())


