from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()


class Genre(models.Model):
    slug = models.SlugField(primary_key=True, max_length=30, blank=True)
    title = models.CharField(max_length=30, unique=True)
    created_at = models.DateField(auto_now_add=True)


@receiver(pre_save, sender=Genre)
def genre_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class Song(models.Model):
    title = models.CharField(max_length=50)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performer')
    image = models.ImageField(upload_to='media/')
    audio_file = models.FileField(upload_to='audio/')
    audio_link = models.CharField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True,)
    genre = models.ForeignKey(Genre, on_delete=models.RESTRICT, related_name='song', null=True, blank=True)
    slug = models.SlugField(max_length=50, primary_key=True, blank=True)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Song)
def song_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='likes')


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favorites')


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
