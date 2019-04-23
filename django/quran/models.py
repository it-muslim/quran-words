"""Models describing abstractions used at Quran app"""
from django.db import models


class Surah(models.Model):
    """Model representing a surah from the Qur’an."""

    number = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    total_ayahs = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}: ({self.number})"


class Ayah(models.Model):
    """Model representing an ayah from the Qur’an."""

    number = models.PositiveIntegerField()
    text = models.TextField()
    surah = models.ForeignKey(
        Surah, on_delete=models.CASCADE, related_name="ayahs"
    )

    def __str__(self):
        return f"{self.surah.number:03d}{self.number:03d}"
