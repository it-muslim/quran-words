'''Models describing abstractions used at Quran app'''
from django.db import migrations, models


class Surah(models.Model):
    '''General information about Surahs'''
    number = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    total_ayahs = models.PositiveIntegerField()


class Ayah(models.Model):
    '''General information about Ayah'''
    number = models.PositiveIntegerField()
    text = models.TextField()
    surah = models.ForeignKey(
        Surah,
        on_delete=models.CASCADE,
        related_name='ayahs')
