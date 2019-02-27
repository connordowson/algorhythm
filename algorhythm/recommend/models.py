from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User


# Create your models here.

# class User(AbstractBaseUser):
#     user_id = models.AutoField(primary_key = True)
#     email = models.CharField('Email', max_length = 75, unique = True)
#     first_name = models.CharField('First name', max_length = 50)
#     last_name = models.CharField('Last name', max_length = 50)
#     password = models.CharField('Password', max_length = 80)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
#     def __str__(self):
#         return 'Name: ' + self.first_name + " " + self.last_name

class Song(models.Model):
    song_id = models.CharField('Song ID', primary_key = True, max_length = 200)
    title = models.CharField('Song title', max_length = 200)
    artist = models.CharField('Artist name', max_length = 200)
    album = models.CharField('Album name', max_length = 200)
    release_date = models.IntegerField('Year of release')
    acousticness = models.FloatField('Acousticness', max_length = 10)
    danceability = models.FloatField('Danceability', max_length = 10)
    energy = models.FloatField('Energy', max_length = 10)
    instrumentalness = models.FloatField('Instrumentalness', max_length = 10)
    key = models.FloatField('Key', max_length = 10)
    liveness = models.FloatField('Liveness', max_length = 10)
    loudness = models.FloatField('Loudness', max_length = 10)
    mode = models.FloatField('Mode', max_length = 10)
    speechiness = models.FloatField('Speechiness', max_length = 10)
    tempo = models.FloatField('Tempo', max_length = 10)
    valence = models.FloatField('Valence', max_length = 10)



class UserTopTracks(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)
    time_range = models.CharField('Time range', max_length = 10)
    
    class Meta:
        unique_together = (('user_id', 'song_id'))
