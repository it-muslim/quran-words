'''Models describing abstractions used at Quran app'''
from django.db import migrations, models
from django.contrib.postgres.fields import ArrayField


class Surah(models.Model):
    '''General information about Surahs'''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    total_ayahs = models.PositiveIntegerField(default=0)


class Ayah(models.Model):
    '''General information about Ayah'''
    id = models.AutoField(primary_key=True, serialize=False)
    ayah = models.PositiveIntegerField(default=0)
    text = ArrayField(
        models.CharField(max_length=255, blank=True),
        blank=True,
        null=True,)
    surah = models.ForeignKey(
        Surah,
        on_delete=models.CASCADE,
        related_name='ayahs')
