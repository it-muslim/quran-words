# -*- coding: utf-8 -*-
'''Here combine the logic for a set of related views in a single class'''

from rest_framework import viewsets
from .models import Surah
from .serializers import SurahSerializer


class SurahViewSet(viewsets.ModelViewSet):
    '''Surahs ViewSet'''
    queryset = Surah.objects.all()
    serializer_class = SurahSerializer
