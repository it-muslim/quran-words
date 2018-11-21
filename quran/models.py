'''Models describing abstractions used at Quran app'''
import os
import json
from django.db import models
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify


class Surah(models.Model):
    '''Model representing a surah from the Qur’an.'''
    number = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    total_ayahs = models.PositiveIntegerField()

    def __str__(self):
        return "%s:(%s)" % (self.name, self.number)


class Ayah(models.Model):
    '''Model representing an ayah from the Qur’an.'''
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
    quality = models.CharField(
        max_length=10, blank=True,
        help_text='This field contain a bitrate of audio file')
    style = models.CharField(
        max_length=20, blank=True,
        help_text='This filed describe style \
        or speed of reading of the reciter')
    slug = models.SlugField(
        help_text="This field is short label for name, \
        containing only letters and hyphens. \
        It's filled automatically during saving.")

    def clean(self, *args, **kwargs):
        # replacing slashes and empty symbols to avoid creating subfolders
        # while audio file upload to media
        self.quality = self.quality.replace('/', 'p').replace(' ', '')
        # validating bitrate quality matching to string like '192kbps'
        bitrate_validator = RegexValidator(
            regex=r'^[\d]{1,3}\w{2}[p|\/]\w$',
            message='The bitrate is wrong',
            code='invalid_bitrate')
        bitrate_validator(self.quality)
        super(Reciter, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        # creating slug from name
        self.slug = slugify(self.name)
        # running redefined full_clean to validate bitrate quality
        self.full_clean()
        super(Reciter, self).save(*args, **kwargs)

    def __str__(self):
        return "%s: %s(%s)" % (self.name, self.style, self.quality)


def audio_directory_path(recitation, filename):
    '''
    Return a path where audio file for a given recitation will be uploaded
    MEDIA_ROOT/<reciter-slug>/<style>/<quality>/<surah-pk>/<ayah-pk>.mp3
    '''
    ayah = recitation.ayah
    surah_number = ayah.surah.number
    file_extension = os.path.splitext(os.path.basename(filename))[1]
    style_dir = os.path.join(
        '/', recitation.reciter.style
    ) if recitation.reciter.style else ''
    quality_dir = os.path.join(
        '/', recitation.reciter.quality
    ) if recitation.reciter.quality else ''
    return '{slug}{style}{quality}/{surah}/{ayah}.{extension}'.format(
        slug=recitation.reciter.slug,
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
    ayah = models.ForeignKey(
        Ayah,
        on_delete=models.CASCADE,
        related_name='recitations'
    )
    reciter = models.ForeignKey(
        Reciter,
        on_delete=models.CASCADE,
        related_name='recitations')
    segments = models.TextField()
    audio = models.FileField(upload_to=audio_directory_path)

    def set_segments(self, segments_list):
        '''set ayah's segments list to field of segments as a string.'''
        self.segments = json.dumps(segments_list, separators=(',', ':'))

    @property
    def get_segments(self):
        '''return list of segments'''
        try:
            segments_list = json.loads(self.segments)
        except json.decoder.JSONDecodeError:
            print("Can't decode segments string")
        else:
            return segments_list

    def __str__(self):
        return "%s:(%s)" % (self.reciter, self.ayah_id)
