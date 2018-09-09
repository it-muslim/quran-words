# -*- coding: utf-8 -*-
'''This module contains Surahs of Holy Quran'''
from django.db import models


class Surah(models.Model):
    '''Surah class with id name and number of ayahs'''
    surah_id = models.AutoField(primary_key=True)
    surah_name = models.CharField(max_length=250)
    surah_ayah_count = models.IntegerField()
