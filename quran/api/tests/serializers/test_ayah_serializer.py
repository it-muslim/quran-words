from django.test import SimpleTestCase

from quran.api.serializers import AyahSerializer


class TestAyahSerializer(SimpleTestCase):
    def test_fields(self):
        expected_fileds = (
            'number',
            'text',
        )
        self.assertCountEqual(AyahSerializer().get_fields().keys(), expected_fileds)
