from rest_framework import viewsets

from ..models import Surah
from .serializers import SurahListSerializer, SurahDetailsSerializer


class SurahListRetrieveView(viewsets.ReadOnlyModelViewSet):
    """
    Get method handler for list of Surahs.

    retrieve:
    Return the surah by given number.

    list:
    Return a list of all the surahs.
    """

    lookup_field = 'number'
    queryset = Surah.objects.all()
    serializer_class = SurahListSerializer

    def get_serializer_class(self):
        """
        Return appreciate serializer class for the given action.

        For action retrieve returns SurahDetailsSerializer
        For action list returns SurahListSerializer
        """
        if self.action == "retrieve":
            return SurahDetailsSerializer
        return super().get_serializer_class()
