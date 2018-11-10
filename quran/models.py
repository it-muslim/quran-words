'''Models describing abstractions used at Quran app'''
from django.db import models
from django.template.defaultfilters import slugify


class Surah(models.Model):
    '''Model representing a surah from the Qur’an.'''
    number = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    total_ayahs = models.PositiveIntegerField()

    def __str__(self):
        return "%s:(%s)" % (self.name, self.number)


class Ayah(models.Model):
    '''Model representing a ayah from the Qur’an.'''
    number = models.PositiveIntegerField()
    text = models.TextField()
    surah = models.ForeignKey(
        Surah,
        on_delete=models.CASCADE,
        related_name='ayahs')

    def __str__(self):
        return "%s: (%s:%s)" % (
            self.surah.name, self.surah.number, self.number)


class Reciter(models.Model):
    '''Model representing a reciter'''
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Reciter, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Recitation(models.Model):
    '''Model representing a recitation of the reciter'''
    url_mask = models.URLField(max_length=250)
    reciter = models.ForeignKey(
        Reciter,
        on_delete=models.CASCADE,
        related_name='recitations')

    def __str__(self):
        return "%s:(%s)" % (self.reciter, self.url_mask)


class TimeCode(models.Model):
    '''Model representing a timecodes of the recitation ayahs'''
    ayah_id = models.PositiveIntegerField()
    segments = models.TextField()
    recitation = models.ForeignKey(
        Recitation,
        on_delete=models.CASCADE,
        related_name='timecodes')

    def __str__(self):
        return "%s:(%s)" % (self.ayah_id, self.segments)
