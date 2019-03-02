from django.test import SimpleTestCase

from quran.api.serializers import SurahListSerializer


class TestSurahListSerializer(SimpleTestCase):
    def test_fields(self):
        expected_fileds = (
            "number",
            "name",
            "total_ayahs",
        )
        self.assertCountEqual(SurahListSerializer().get_fields().keys(), expected_fileds)
