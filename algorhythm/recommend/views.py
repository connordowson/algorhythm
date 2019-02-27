from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Song, UserTopTracks
import spotipy
import spotipy.util as util
from datetime import datetime


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
        results = spotify.current_user_top_tracks(limit=50, offset=0, time_range=time_range)

        tracks_list = []
        audio_features = []

        top_tracks = results['items']

        for index, track in enumerate(results['items']):
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
            this_audio_features = {}
            results = spotify.audio_features(track['id'])
            track_info['audio_features'] = results[0]

            # Add list of tracks to variable to be used in context
            tracks_list.append(track_info)
            
    return tracks_list

@login_required
def recommend(request):
   
    context = {
        'current_user': request.user.first_name,
        'top_tracks': 'empty'
    }

    if(request.GET.get('long_term')):
        top_tracks = get_top_tracks('long_term')
        context.update({'top_tracks': top_tracks})

    if(request.GET.get('medium_term')):
        top_tracks = get_top_tracks('medium_term')
    
    if(request.GET.get('short_term')):
        top_tracks = get_top_tracks('short_term')


    # upload_songs(request.user.id, get_top_tracks('long_term'), 'Long term')

    return render(request, 'recommend/recommend.html', context=context)

def upload_songs(user_id, songs, time_range):

    this_user = User.objects.get(id = user_id)

    for track in songs:

        this_song_id = track['song_id']

        if not Song.objects.filter(song_id = this_song_id).exists():
            this_song = Song.objects.create(
                song_id = this_song_id,
                title = track['title'],
                artist = track['artist'],
                album = track['album'],
                release_date = track['release_date'],
                acousticness = track['audio_features']['acousticness'],
                danceability = track['audio_features']['danceability'],
                energy = track['audio_features']['energy'],
                instrumentalness = track['audio_features']['instrumentalness'],
                key = track['audio_features']['key'],
                liveness = track['audio_features']['liveness'],
                loudness = track['audio_features']['loudness'],
                mode = track['audio_features']['mode'],
                speechiness = track['audio_features']['speechiness'],
                tempo = track['audio_features']['tempo'],
                valence = track['audio_features']['valence']
            )
            this_song.save()

        if not UserTopTracks.objects.filter(user_id = user_id, song_id = this_song_id, time_range = time_range).exists():

            this_song = Song.objects.get(song_id = this_song_id)

            this_top_tracks = UserTopTracks.objects.create(
                user_id = this_user,
                song_id = this_song,
                time_range = time_range
            )
            this_top_tracks.save()



def index(request):
    return render(request, 'recommend/index.html')
