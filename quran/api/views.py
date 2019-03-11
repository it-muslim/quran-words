from rest_framework import viewsets

from ..models import Surah
from .serializers import SurahListSerializer, SurahDetailsSerializer


class SurahListRetrieveView(viewsets.ReadOnlyModelViewSet):
    """View that allows to list and retrieve Surah."""
    lookup_field = 'number'
    queryset = Surah.objects.all()
    serializer_class = SurahListSerializer

    def get_serializer_class(self):
        """
        Returns appreciate serializer class for the given action.

        For action retrieve returns SurahDetailsSerializer
        For action list returns SurahListSerializer
        """
        if self.action == "retrieve":
            return SurahDetailsSerializer
        return super().get_serializer_class()
