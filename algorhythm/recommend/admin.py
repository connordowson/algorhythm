from django.contrib import admin

# Register your models here.

# from .models import User
from django.contrib.auth.models import User
from .models import Song, UserTopTracks

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name')
    ordering = ('id',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class SongAdmin(admin.ModelAdmin):
    list_display = ('song_id', 'title', 'artist', 'album', 'release_date')
    ordering = ('song_id',)

admin.site.register(Song, SongAdmin)

class UserTopTracksAdmin(admin.ModelAdmin):
    list_display = ('song_id', 'user_id', 'time_range')

admin.site.register(UserTopTracks, UserTopTracksAdmin)
