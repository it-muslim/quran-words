'''Models describing abstractions used at Quran app'''
from django.db import models
import django.contrib.postgres.fields
from django.contrib.postgres.fields import ArrayField


class Surah(models.Model):
    '''General information about Surahs'''
    surah_id = models.AutoField(primary_key=True)
    surah_name = models.CharField(max_length=20)
    surah_ayah_count = models.PositiveIntegerField()


class Ayah(models.Model):
    '''General information about Ayah'''
    ayah_id = models.AutoField(primary_key=True)
    ayah_text = ArrayField(
        models.CharField(max_length=255, blank=True, default=''),
        default=list)
    surah = models.ForeignKey(
        'quran.Surah',
        on_delete=models.CASCADE,
        related_name='ayahs',
        default=1)
