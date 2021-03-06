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


    # create url to authorize user
    def get_authorize_url(self):

        queries = {'client_id': self.client_id, 'redirect_uri': self.redirect_uri, 'scope': self.scope, 'response_type': 'code', 'show_dialog:' : 'true'}

        urlparams = urllib.parse.urlencode(queries)

        url = "%s?%s" % (self.AUTHORIZE_URL, urlparams)

        return(url)


    # make call to get token
    def get_authorize_token(self, code):

        headers = make_authorization_headers(self.client_id, self.client_secret)

        queries = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': self.redirect_uri}

        response = requests.post(self.TOKEN_URL, data = queries, headers = headers)

        token_info = response.json()

        return(token_info['access_token'])


    # api call to get users top tracks
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

        # for each song that was returned add the relevant info to a list so it can be rendered on the page
        for index, track in enumerate(top_tracks):

            # Check if song info is already on the database
            if not(Song.objects.filter(song_id = track['id']).exists()):

                track_info = {}
                track_info['song_id'] = track['id']
                track_info['title'] = track['name']
                track_info['artist'] = track['artists'][0]['name']
                track_info['album'] = track['album']['name']
                track_info['image_url'] = track['album']['images'][2]['url']

                release_date_precision = track['album']['release_date_precision']

                if(release_date_precision == "year"):
                    track_info['release_date'] = int(track['album']['release_date'])
                else:               
                    formatted_date = datetime.strptime(track['album']['release_date'], '%Y-%m-%d')
                    year = formatted_date.year
                    track_info['release_date'] = int(year)

                # Get audio features for users top songs
                audio_features = self.get_audio_features(track['id'], token)

                track_info['audio_features'] = audio_features

                # Add list of tracks to variable to be used in context
                tracks_list.append(track_info)
            # if song is already in the databasse get info from databse, except for the picture
            else:
                this_song = Song.objects.get(song_id = track['id'])
                track_info = {}
                track_info['song_id'] = getattr(this_song, 'song_id')
                track_info['title'] = getattr(this_song, 'title')
                track_info['artist'] = getattr(this_song, 'artist')
                track_info['image_url'] = track['album']['images'][2]['url']
                tracks_list.append(track_info)

        return tracks_list

    # call api to get audio features for the song given in parameters
    def get_audio_features(self, song_id, token):

        endpoint = 'https://api.spotify.com/v1/audio-features/'

        url = endpoint + song_id

        headers = {'Authorization': 'Bearer {0}'.format(token), 'Accept': 'application/json', 'Content-Type' : 'application/json'}

        results = requests.get(url, headers = headers)

        return(results.json())

    # create a playlist containing all the songs passed in
    def make_playlist(self, token, songs):

        endpoint = 'https://api.spotify.com/v1/me/'

        url = endpoint

        headers = {'Authorization': 'Bearer {0}'.format(token)}

        results = requests.get(url, headers = headers)

        results = results.json()

        spotify_id = results['id']

        endpoint = 'https://api.spotify.com/v1/users/{0}/playlists'.format(spotify_id)

        headers = {'Authorization': 'Bearer {0}'.format(token), 'Content-Type' : 'application/json'}

        queries = {
            'name': 'Algorhythm Recommendations',
            'description': 'Playlist made from recommendations at https://algorhythm.connordowson.com/',
        }

        queries = json.dumps(queries)

        results = requests.post(endpoint, headers = headers, data = queries)

        playlist_id = results.json()['id']

        endpoint = 'https://api.spotify.com/v1/playlists/{0}/tracks'.format(playlist_id)

        songs_to_add = []

        for song in songs:
            songs_to_add.append("spotify:track:{0}".format(song.song_id.song_id))

        queries = {

            'uris': songs_to_add

        }

        queries = json.dumps(queries)

        results = requests.post(endpoint, headers = headers, data = queries)

        return(spotify_id, playlist_id)






