from rest_framework import exceptions, status, viewsets

from ..models import Recitation, Reciter
from .serializers import RecitationSerializer, ReciterSerializer


class UnprocessableEntityError(exceptions.APIException):
    """Extend DRF API exceptions to manage unprocessable entities."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Query for surah_number and reciter_id not found."


class ReciterListRetrieveView(viewsets.ReadOnlyModelViewSet):
    """Get method handler for list of Reciters."""

    lookup_field = 'id'
    queryset = Reciter.objects.all()
    serializer_class = ReciterSerializer


class RecitationListRetrieveView(viewsets.ReadOnlyModelViewSet):
    """Get method handler for list of Recitations."""

    serializer_class = RecitationSerializer

    def get_queryset(self):
        """Filter recitations from request queries."""
        reciter_id = self.request.query_params.get('reciter_id')
        surah_number = self.request.query_params.get('surah_number')

        if not reciter_id or not surah_number:
            raise UnprocessableEntityError()

        recitations = Recitation.objects.filter(
            surah=surah_number, reciter=reciter_id)

        if recitations:
            return recitations
        raise exceptions.NotFound()
