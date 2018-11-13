'''Models describing abstractions used at Quran app'''
from os import path
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
    quality = models.CharField(max_length=20, blank=True)
    style = models.CharField(max_length=100, blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.quality = self.quality.replace('/', 'p').replace(' ', '')
        self.slug = slugify(self.name)
        super(Reciter, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def audio_directory_path(instance, filename):
    '''
    the function generates path for
    uploading audio file of ayahs to
    MEDIA_ROOT/<reciter-slug>/<style>/<quality>/<surah-id>/<ayah-id>.mp3
    '''
    ayah = Ayah.objects.get(pk=instance.ayah_id)
    surah_number = ayah.surah.number
    file_extension = path.splitext(path.basename(filename))[1]
    style_dir = path.join(
        '/', instance.reciter.style
    ) if instance.reciter.style else ''
    quality_dir = path.join(
        '/', instance.reciter.quality
    ) if instance.reciter.quality else ''
    return '{slug}{style}{quality}/{surah}/{ayah}.{extension}'.format(
        slug=instance.reciter.slug,
        style=style_dir,
        quality=quality_dir,
        surah=surah_number,
        ayah=ayah.number,
        extension=file_extension
    )


class Recitation(models.Model):
    '''
    This model represents a recitation of an ayah from the Qur'an.
    Each recitation has an audio file and time segments which hold
    an information about times when each word in this audio file
    was pronounced.
    '''
    ayah_id = models.PositiveIntegerField()
    segments = models.TextField()
    audio = models.FileField(upload_to=audio_directory_path)
    reciter = models.ForeignKey(
        Reciter,
        on_delete=models.CASCADE,
        related_name='recitations')

    def __str__(self):
        return "%s:(%s)" % (self.reciter, self.ayah_id)
