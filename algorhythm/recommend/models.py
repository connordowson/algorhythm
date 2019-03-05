from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager
from django.utils import timezone
# Create your models here.

class UserManager(AbstractUserManager):

    def create_user(self, email, first_name, last_name, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email = email, is_staff = False, is_active = False, is_superuser = False, last_login = now, date_joined = now, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, first_name, last_name, password, True, True, **extra_fields)
        
        user.is_active=True
        user.save()
        return user

class User(AbstractUser):
    username = None
    access_code = models.CharField('Spotify API access code', max_length = 300)
    email = models.EmailField(max_length = 254, unique = True)
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return 'Name: ' + self.first_name + " " + self.last_name

    objects = UserManager()


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
    time_range = models.CharField('Time range', max_length = 11)
    
    class Meta:
        unique_together = (('user_id', 'song_id', 'time_range'))
