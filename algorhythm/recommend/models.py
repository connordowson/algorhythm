from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    email = models.CharField('email', max_length = 75)
    first_name = models.CharField('First name', max_length = 50)
    last_name = models.CharField('Last name', max_length = 50)
    password = models.CharField('Password', max_length = 50)
    def __str__(self):
        return 'Name: ' + self.first_name + " " + self.last_name 

class Song(models.Model):
    song_id = models.IntegerField(primary_key = True)
    title = models.CharField('Song title', max_length = 200)
    artist = models.CharField('Artist name', max_length = 200)
    album = models.CharField('Album name', max_length = 200)
    release_date = models.DateField('Date of release')


class Playlist(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    song_id = models.ForeignKey(Song, on_delete = models.CASCADE)
    
    class Meta:
        unique_together = (('user_id', 'song_id'))
