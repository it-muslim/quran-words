'''Models describing abstractions used at Quran app'''
import os
from django.db import models
from django.template.defaultfilters import slugify


class Surah(models.Model):
    '''Model representing a surah from the Qur’an.'''
    number = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    total_ayahs = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}: ({self.number})'


class Ayah(models.Model):
    '''Model representing an ayah from the Qur’an.'''
    number = models.PositiveIntegerField()
    text = models.TextField()
    surah = models.ForeignKey(
        Surah,
        on_delete=models.CASCADE,
        related_name='ayahs')

    def __str__(self):
        return f'{self.surah.name}: ({self.surah.number}:{self.number})'


class Reciter(models.Model):
    '''Model representing a reciter'''
    name = models.CharField(max_length=100)
    bitrate = models.PositiveIntegerField(
        blank=True,
        help_text='This field contain a bitrate of audio file')
    style = models.CharField(
        max_length=20, blank=True,
        help_text='This filed describe style \
        or speed of reading of the reciter')
    slug = models.SlugField(
        help_text="This field is short label for name, \
        containing only letters and hyphens. \
        It's filled automatically during saving.")

    def save(self, *args, **kwargs):
        # creating slug from name
        self.slug = slugify(self.name)
        super(Reciter, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}: {self.style}({self.bitrate}kb/s)'


def audio_directory_path(recitation, filename):
    '''
    Return a path where audio file for a given recitation will be uploaded
    MEDIA_ROOT/<reciter-slug>/<style>/<bitrate>/<surah-pk>/<ayah-pk>.mp3
    '''
    ayah = recitation.ayah
    file_extension = os.path.splitext(os.path.basename(filename))[1]
    return os.path.join(
        recitation.reciter.slug,
        recitation.reciter.style,
        f'{recitation.reciter.bitrate}kbps',
        f'{ayah.surah.number}',
        f'{ayah.number}{file_extension}'
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

    def __str__(self):
        return f'{self.reciter}: ({self.ayah})'

    def set_segments(self, segments_list):
        '''
        set ayah's segments list containing tuples
        of timecodes pair of beginning and ending
        of the word to field of segments as a string.
        '''
        self.segments = ','.join(
            (f'{segment_pair[0]}:{segment_pair[1]}'
                for segment_pair in segments_list))

    @property
    def get_segments(self):
        '''return list of segments containing tuple of timecodes'''
        return [
            tuple(int(timecode) for timecode in timecodes.split(':'))
            for timecodes in self.segments.split(',')]
