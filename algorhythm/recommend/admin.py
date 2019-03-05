from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# from .models import User
from .models import User, Song, UserTopTracks
admin.site.register(User)

class SongAdmin(admin.ModelAdmin):
    list_display = ('song_id', 'title', 'artist', 'album', 'release_date')
    ordering = ('song_id',)

admin.site.register(Song, SongAdmin)

class UserTopTracksAdmin(admin.ModelAdmin):
    list_display = ('song_id', 'user_id', 'time_range')

admin.site.register(UserTopTracks, UserTopTracksAdmin)
