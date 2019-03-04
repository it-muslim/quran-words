from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

from .models import Surah, Ayah
from .serializers import SurahSerializer, AyahSerializer


class GetQuran(APITestCase):
    '''Checking Quran app API'''

    def test_nonexistent_surah(self):
        '''
        Checks 404 response to non-existent surahs
        '''
        response = self.client.get(
            reverse(
                "surah-details",
                kwargs={
                    "number": 115
                }
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
