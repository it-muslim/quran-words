'''Models describing abastractions used at Quran app'''
from django.db import models


class Surah(models.Model):
    '''General information about Surahs'''
    surah_id = models.AutoField(primary_key=True)
    surah_name = models.CharField(max_length=20)
    surah_ayah_count = models.PositiveIntegerField()
