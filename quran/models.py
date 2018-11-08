'''Models describing abstractions used at Quran app'''
from django.db import models


class Surah(models.Model):

    ''' General information about Surah '''

    number = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    total_ayahs = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Ayah(models.Model):

    ''' General information about Ayah '''

    number = models.PositiveIntegerField()
    text = models.TextField()
    surah = models.ForeignKey(
        Surah,
        on_delete=models.CASCADE,
        related_name='ayahs')

    def __str__(self):
        return "%s:%s" % (self.surah.name, self.number)
