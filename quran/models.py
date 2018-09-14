'''Models describing abstractions used at Quran app'''
from django.db import models
import django.contrib.postgres.fields
from django.contrib.postgres.fields import ArrayField


class Surah(models.Model):
    '''General information about Surahs'''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    total_ayahs = models.PositiveIntegerField()


class Ayah(models.Model):
    '''General information about Ayah'''
    id = models.AutoField(primary_key=True)
    text = ArrayField(
        models.CharField(max_length=255, blank=True, default=''),
        default=list)
    surah = models.ForeignKey(
        Surah,
        on_delete=models.CASCADE,
        related_name='ayahs',
        default=1)
