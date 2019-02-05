"""Models describing abstractions used for Recite app"""
import os

from django.db import models
from django.template.defaultfilters import slugify

from .fields import SegmentsField


class Reciter(models.Model):
    """Model representing a reciter"""

    name = models.CharField(max_length=100)
    bitrate = models.PositiveIntegerField(
        blank=True, null=True, help_text="Bitrate of an audio file"
    )
    style = models.CharField(
        max_length=20, blank=True, help_text="Qur'an reading style"
    )
    slug = models.SlugField(
        help_text="Short label for name, "
        "containing only letters and hyphens. "
        "It's filled automatically during saving."
    )

    def save(self, *args, **kwargs):
        # creating slug from name
        self.slug = slugify(self.name)
        super(Reciter, self).save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.name} "
            f"(style={self.style or None}, bitrate={self.bitrate})"
        )


def audio_directory_path(recitation, filename):
    """
    Return a path where audio file for a given recitation will be uploaded
    MEDIA_ROOT/<reciter-slug>/<style>/<bitrate>/<surah-number>/<ayah-number>.mp3
    """
    ayah = recitation.ayah
    file_extension = os.path.splitext(os.path.basename(filename))[1]
    bitrate = (
        f"{recitation.reciter.bitrate}kbps"
        if recitation.reciter.bitrate
        else ""
    )
    return os.path.join(
        recitation.reciter.slug,
        recitation.reciter.style,
        bitrate,
        f"{ayah.surah.number}",
        f"{ayah.number}{file_extension}",
    )


class Recitation(models.Model):
    """
    This model represents a recitation of an ayah from the Qur'an.
    Each recitation has an audio file and time segments which hold
    an information about times when each word in this audio file
    was pronounced.
    """

    ayah = models.ForeignKey(
        'quran.Ayah', on_delete=models.CASCADE, related_name="recitations"
    )
    reciter = models.ForeignKey(
        Reciter, on_delete=models.CASCADE, related_name="recitations"
    )
    segments = SegmentsField()
    audio = models.FileField(upload_to=audio_directory_path)

    def __str__(self):
        return f"{self.reciter}: ({self.ayah})"
