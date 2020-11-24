from rest_framework import exceptions, mixins, schemas, status, viewsets

from ..models import Recitation, Reciter
from .serializers import RecitationSerializer, ReciterSerializer
from rest_framework.schemas.openapi import AutoSchema


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

    class ReciterSchema(AutoSchema):

        def get_operation(self, path, method):
            operation = super().get_operation(path, method)

            operation["parameters"].append({
                "name": "reciter_id",
                "in": "query",
                "required": True,
                "description": "Reciter id",
                'schema': {'type': 'string'}
            })

            operation["parameters"].append({
                "name": "surah_number",
                "in": "query",
                "required": True,
                "description": "Surah number",
                'schema': {'type': 'string'}
            })
            return operation

    schema = ReciterSchema()
