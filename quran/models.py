'''Models describing abstractions used at Quran app'''
from django.db import migrations, models


class Surah(models.Model):
    '''General information about Surahs'''
    name = models.CharField(max_length=20)
    total_ayahs = models.PositiveIntegerField(default=0)


class Ayah(models.Model):
    '''General information about Ayah'''
    ayah = models.PositiveIntegerField(default=0)
    text = models.TextField()
    surah = models.ForeignKey(
        Surah,
        on_delete=models.CASCADE,
        related_name='ayahs')
