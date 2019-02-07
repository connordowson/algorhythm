from django.shortcuts import render
from django.http import HttpResponse
import spotipy
import spotipy.util as util

username = '1114744532'
scope = 'user-top-read'
client_id = '***REMOVED***'
client_secret = '***REMOVED***'
redirect_uri = 'http://localhost:8000/recommend/'
oauth = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

# Create your views here.

def get_top_tracks(time_range):
    if oauth:
        spotify = spotipy.Spotify(auth=oauth)
        results = spotify.current_user_top_tracks(limit=25, offset=0, time_range=time_range)

        tracks_list = []

        top_tracks = results['items']

        for index, track in enumerate(results['items']):
            track_info = {}
            track_info['title'] = track['name']
            track_info['artist'] = track['artists'][0]['name']
            track_info['image_url'] = track['album']['images'][0]['url']
            tracks_list.append(track_info)
    
    return tracks_list

def index(request):

    context = {
        'short_term_top_tracks': get_top_tracks('short_term'),
        'medium_term_top_tracks': get_top_tracks('medium_term'),
        'long_term_top_tracks': get_top_tracks('long_term')
    }

    return render(request, 'index.html', context=context) 