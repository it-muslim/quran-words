from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

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
    serializer_class = serializers.SurahSerializer

    def get(self, request, *args, **kwargs):
        try:
            surah = self.queryset.get(pk=kwargs["surah_id"])
            return Response(serializers.SurahDetailsSerializer(surah).data)
        except Surah.DoesNotExist:
            return Response(
                data={
                    "message":
                    "Surah with id: {} does not exist".format(
                        kwargs["surah_id"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
