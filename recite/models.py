"""Models describing abstractions used for Recite app"""
import os

from django.db import models

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
        unique=True,
        help_text="Short unique label for name, "
        "containing only letters and hyphens. "
    )

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
            self.reciter.slug,
            f"{self.ayah.surah.number:03d}",
            f"{self.ayah.number:03d}"
            f"{file_extension}",
        )

    audio = models.FileField(
        upload_to=get_audio_directory)

    def __str__(self):
        return f"{self.reciter}: ({self.ayah})"
