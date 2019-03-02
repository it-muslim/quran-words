from django.test import SimpleTestCase

from quran.api.serializers import SurahDetailsSerializer


class TestSurahDetailsSerializer(SimpleTestCase):
    def test_fields(self):
        expected_fileds = (
            "number",
            "name",
            "total_ayahs",
            "ayahs",
        )
        self.assertCountEqual(SurahDetailsSerializer().get_fields().keys(), expected_fileds)
