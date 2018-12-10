import shutil
import tempfile
from django.conf import settings
from django.test import TestCase
from django.core.files import File
from .models import Ayah, Reciter, Recitation


class ReciterTestCase(TestCase):
    """Tests for Reciter model"""

    def setUp(self):
        # create the reciter object
        self.mishari = Reciter.objects.create(name="Mishari Rashid al-ʿAfasi")

    def test_reciter_string_representation(self):
        self.assertEqual(
            str(self.mishari),
            "Mishari Rashid al-ʿAfasi (style=None, bitrate=None)",
        )

    def test_reciter_string_representation_with_style(self):
        self.mishari.style = "murattal"
        self.assertEqual(
            str(self.mishari),
            "Mishari Rashid al-ʿAfasi (style=murattal, bitrate=None)",
        )

    def test_reciter_string_representation_with_style_and_bitrate(self):
        self.mishari.style = "murattal"
        self.mishari.bitrate = 128
        self.assertEqual(
            str(self.mishari),
            "Mishari Rashid al-ʿAfasi (style=murattal, bitrate=128)",
        )

    def test_reciter_slug(self):
        self.assertEqual(self.mishari.slug, "mishari-rashid-al-afasi")


class RecitationTestCase(TestCase):
    """Test for Recitation model"""

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self._original_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = self.test_dir
        # get the second ayah from the surah Al-Baqara
        self.ayah = Ayah.objects.get(pk=8)
        # create a temporary audio
        file = tempfile.NamedTemporaryFile(suffix=".mp3")
        self.audio_ayah = File(file, name=file.name)
        # create a reciter
        self.mishari = Reciter.objects.create(name="Mishari Rashid al-ʿAfasi")

    def tearDown(self):
        # Delete a temporary directory
        shutil.rmtree(self.test_dir)
        settings.MEDIA_ROOT = self._original_media_root

    def test_recitation_audio_path_with_name_only(self):
        recitation = Recitation.objects.create(
            ayah=self.ayah,
            segments="",
            reciter=self.mishari,
            audio=self.audio_ayah,
        )
        self.assertEqual(recitation.audio, "mishari-rashid-al-afasi/2/1.mp3")

    def test_recitation_audio_path_with_name_and_bitrate(self):
        self.mishari.bitrate = 128
        recitation = Recitation.objects.create(
            ayah=self.ayah,
            segments="",
            reciter=self.mishari,
            audio=self.audio_ayah,
        )
        self.assertEqual(
            recitation.audio, "mishari-rashid-al-afasi/128kbps/2/1.mp3"
        )

    def test_recitation_audio_path_with_name_and_style(self):
        self.mishari.style = "murattal"
        recitation = Recitation.objects.create(
            ayah=self.ayah,
            segments="",
            reciter=self.mishari,
            audio=self.audio_ayah,
        )
        self.assertEqual(
            recitation.audio, "mishari-rashid-al-afasi/murattal/2/1.mp3"
        )

    def test_recitation_audio_path_with_name_style_and_bitrate(self):
        self.mishari.bitrate = 128
        self.mishari.style = "mujawwad"
        recitation = Recitation.objects.create(
            ayah=self.ayah,
            segments="",
            reciter=self.mishari,
            audio=self.audio_ayah,
        )
        self.assertEqual(
            recitation.audio,
            "mishari-rashid-al-afasi/mujawwad/128kbps/2/1.mp3",
        )
