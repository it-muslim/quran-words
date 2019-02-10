"""Models describing abstractions used for Recite app"""
from django.db import models
from django.template.defaultfilters import slugify

from .fields import SegmentsField
import os


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

    def get_audio_directory(self, filename):
        file_extension = os.path.splitext(os.path.basename(filename))[1]
        return os.path.join(
            "recite",
            f"{self.reciter_id}",
            f"{str(self.ayah)}"
            f"{file_extension}",
        )

    audio = models.FileField(
        upload_to=get_audio_directory)

    def __str__(self):
        return f"{self.reciter}: ({self.ayah})"
