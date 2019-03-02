from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from quran.api.serializers import SurahListSerializer, SurahDetailsSerializer
from quran.models import Surah


class TestSurahListRetrieveView(APITestCase):

    def setUp(self):
        self.list_url = reverse("api:quran-list")
        self.surah_number = 1
        self.details_url = reverse("api:quran-detail", kwargs={"number": self.surah_number})

    def test_list_url(self):
        self.assertEqual(self.list_url, "/api/quran/surah/")

    def test_details_url(self):
        self.assertEqual(self.details_url, "/api/quran/surah/1/")

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 114)

        serializer = SurahListSerializer(Surah.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)

    def test_details(self):
        response = self.client.get(self.details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = SurahDetailsSerializer(Surah.objects.get(number=self.surah_number))
        self.assertCountEqual(response.data, serializer.data)
