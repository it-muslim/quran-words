from rest_framework import viewsets

from ..models import Surah
from .serializers import SurahListSerializer, SuraDetailsSerializer


class SurahListRetrieveView(viewsets.ReadOnlyModelViewSet):
    """View that allows to List, Retrieve Surah."""
    lookup_field = 'number'
    queryset = Surah.objects.all()
    serializer_class = SurahListSerializer

    def get_serializer_class(self):
        """Returns appreciate serializer class for the given action."""
        if self.action == "retrieve":
            return SuraDetailsSerializer
        return super().get_serializer_class()
