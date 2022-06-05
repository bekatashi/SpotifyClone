from django.db import models
from song.models import Song
from django.contrib.auth import get_user_model
User = get_user_model()

marks = (
        (1, 'Looser of loosers'),
        (2, 'Looser'),
        (3, 'Satisfied'),
        (4, "Good"),
        (5, 'Perfect')
)


class Ratings(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')
    mark = models.PositiveSmallIntegerField(choices=marks)

    class Meta:
        verbose_name = 'rating'
        unique_together = ('owner', 'song')

    def __str__(self): return f'{self.mark} -> {self.song}'
