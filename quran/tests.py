from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

from .models import Surah, Ayah
from .serializers import SurahSerializer, AyahSerializer


class GetQuran(APITestCase):
    '''Checking Quran app API'''
    client = APIClient()

    def test_get_surahs(self):
        '''
        This test ensures that surahs is loaded correctly to database
        making a GET request to the quran/ endpoint
        '''
        # hit the API endpoint
        response = self.client.get(
            reverse("surahs-all")
        )
        # fetch the data from db
        expected = Surah.objects.all()
        serialized = SurahSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check number of Surahs
        self.assertEqual(len(response.data), 114)

    def test_get_ayahs_of_surahs(self):
        '''
        This test ensures that ayahs is loaded correctly to database
        making a GET request to the quran/{surah_id} endpoint
        '''
        # hit the API endpoint for each surah
        surahs = list(range(1, 115))

        for surah_id in surahs:
            response = self.client.get(
                reverse(
                    "surah-details",
                    kwargs={
                        "surah_id": surah_id
                    }
                )
            )
            # fetch the data from db
            expected = Ayah.objects.filter(surah=surah_id)
            serialized = AyahSerializer(expected, many=True)

            self.assertEqual(response.data['ayahs'], serialized.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_nonexistent_surah(self):
        '''
        Checks 404 response to non-existent surahs
        '''
        response = self.client.get(
            reverse(
                "surah-details",
                kwargs={
                    "surah_id": 115
                }
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
