from rest_framework import generics

from . import serializers
from .models import Surah


class SurahListView(generics.ListAPIView):
    """
    Provides a get method handler for Surah list.
    """
    queryset = Surah.objects.all()
    serializer_class = serializers.SurahSerializer


class SurahDetailsView(generics.RetrieveAPIView):
    """
    Provides a get method handler for Surah details.
    """
    queryset = Surah.objects.all()
    serializer_class = serializers.SurahDetailsSerializer
    lookup_field = 'number'
