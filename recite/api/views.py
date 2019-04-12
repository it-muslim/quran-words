import coreapi
import coreschema
from rest_framework import exceptions, mixins, schemas, status, viewsets

from ..models import Recitation, Reciter
from .serializers import RecitationSerializer, ReciterSerializer


class UnprocessableEntityError(exceptions.APIException):
    """Extend DRF API exceptions to manage unprocessable entities."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Query for surah_number and reciter_id not found."


class ReciterListRetrieveView(viewsets.ReadOnlyModelViewSet):
    """
    Get method handler for list of Reciters.

    retrieve:
    Return the reciter by given id.

    list:
    Return a list of all the reciters.
    """

    lookup_field = 'id'
    queryset = Reciter.objects.all()
    serializer_class = ReciterSerializer


class RecitationListRetrieveView(
        viewsets.GenericViewSet,
        mixins.ListModelMixin):
    """
    Get method handler for list of Recitations.

    list:
    Return a list of the recitations for given reciter and given surah.
    """

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

    # Custom schema for core api documentation.
    schema = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                'reciter_id',
                True,
                "query",
                coreschema.Integer(
                    title='Reciter id',
                    description='A unique integer value identifying reciter.',
                ),
            ),
            coreapi.Field(
                'surah_number',
                True,
                "query",
                coreschema.Integer(
                    title='Surah number',
                    description='A unique integer value identifying surah.',
                ),
            ),
        ]
    )
