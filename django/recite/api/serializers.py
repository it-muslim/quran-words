from rest_framework import serializers
from recite.models import Recitation, Reciter


class SegmentsListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value


class ReciterSerializer(serializers.ModelSerializer):
    """Serializer for Reciter model."""

    class Meta:
        model = Reciter
        fields = '__all__'


class RecitationSerializer(serializers.ModelSerializer):
    """Serializer for Recitation model."""

    # Send surah, ayah numbers instead of their pk
    ayah = serializers.IntegerField(source='ayah.number', read_only=True)
    surah = serializers.IntegerField(source='surah.number', read_only=True)
    segments = SegmentsListingField(many=True, read_only=True)

    class Meta:
        model = Recitation
        fields = ('surah', 'ayah', 'segments', 'audio', 'reciter')
