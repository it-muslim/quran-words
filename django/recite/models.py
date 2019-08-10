"""Models describing abstractions used for Recite app"""
import os
import shutil

from django.db import models

from .fields import SegmentsField
from django.dispatch import receiver
from django.conf import settings


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
    surah = models.ForeignKey(
        'quran.Surah', on_delete=models.CASCADE, related_name="recitations"
    )
    ayah = models.ForeignKey(
        'quran.Ayah', on_delete=models.CASCADE, related_name="recitations"
    )
    reciter = models.ForeignKey(
        Reciter, on_delete=models.CASCADE, related_name="recitations"
    )
    segments = SegmentsField()
    audio = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.reciter}: ({self.ayah})"

    class Meta:
        ordering = ['ayah']


@receiver(models.signals.post_delete, sender=Reciter)
def auto_delete_files_on_delete(sender, instance, **kwargs):
    """
    Deletes Recitation files from the filesystem
    when the corresponding `Reciter` object is deleted.
    """
    reciter_path = os.path.join(
        settings.MEDIA_ROOT, 'recite', str(instance.slug))
    if os.path.exists(reciter_path):
        shutil.rmtree(reciter_path)
