from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from quran.api.serializers import SurahListSerializer, SurahDetailsSerializer
from quran.models import Surah


class TestSurahListRetrieveView(APITestCase):

    def test_list(self):
        MAX_SURAH_NUMBER = 114
        url = reverse("api:quran-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), MAX_SURAH_NUMBER)

        serializer = SurahListSerializer(Surah.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)

    def test_details(self):
        SURAH_NUMBER = 1
        url = reverse("api:quran-detail", kwargs={"number": SURAH_NUMBER})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = SurahDetailsSerializer(Surah.objects.get(number=SURAH_NUMBER))
        self.assertCountEqual(response.data, serializer.data)
