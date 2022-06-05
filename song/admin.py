from django.contrib import admin
from .models import Song, Like, Favorite, Genre
admin.site.register(Song)
admin.site.register(Favorite)
admin.site.register(Like)
admin.site.register(Genre)
