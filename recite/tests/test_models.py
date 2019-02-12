from django.test import TestCase

from recite.models import Reciter


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
