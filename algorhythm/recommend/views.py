from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Song, UserTopTracks, User
import spotipy
import spotipy.util as util
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
from . import spotify_wrapper
from http import cookies


username = '1114744532'
# username = '1123375424'
scope = 'user-top-read playlist-modify-public'
client_id = '***REMOVED***'
client_secret = '***REMOVED***'
redirect_uri = 'http://localhost:8000/recommend/'
# sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret ,redirect_uri, scope)
auth = spotify_wrapper.SpotifyWrapper(client_id, client_secret, redirect_uri, scope)


# Create your views here.

@login_required
def recommend(request):

    auth = spotify_wrapper.SpotifyWrapper(client_id, client_secret, redirect_uri, scope)

    context = {
        'current_user': request.user.first_name,
    }

    if(request.method == 'GET'):

        if(request.GET.get('code')):

            code = request.GET.get('code')
            current_user = request.user


            request.session[str(current_user.id)] = code

            context = {
                'current_user': current_user.first_name,
                'code': code
            }

            return render(request, 'recommend/recommend.html', context = context)

        else:
            auth.get_authorize_url()
            return render(request, 'recommend/recommend.html', context = context)
       
    return render(request, 'recommend/recommend.html')

@login_required
def short_term(request):

    user_id = request.user.id

    code = request.session[str(user_id)]

    token = auth.get_authorize_token(code)

    results = auth.get_top_tracks(token, 'long_term')

    context = {
        'code': results,
        'token': token
    } 
    
    return render(request, 'recommend/top_tracks.html', context = context)


@login_required
def top_tracks(request):

    # if request.method == 'GET':

    #     time_range = request.GET.get('time_range')
    #     current_user_id = request.user.id
    #     top_tracks = get_top_tracks(time_range, current_user_id)

    #     context = {
    #         'top_tracks': get_top_tracks(time_range),
    #         'time_range': time_range,
    #     }

    #     upload_songs(request.user.id, top_tracks, time_range)

    #     return render(request, 'recommend/top_tracks/', context = context)

    return render(request, 'recommend.html')

def sign_in_to_spotify(request):

    if request.method == 'GET':

        code = request.GET.get('code')

        current_user = request.user.id

        this_user = User.objects.get(id = current_user)
        this_user.access_token = code
        this_user.save()

    return redirect('/recommend/')

# @login_required
def get_top_tracks(time_range, current_user_id):

    # oauth = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    

# def upload_songs(user_id, songs, time_range):

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


# @login_required
def index(request):
    return render(request, 'recommend/index.html')
