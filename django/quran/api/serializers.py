from rest_framework import serializers

from quran.models import Ayah, Surah


class SurahListSerializer(serializers.ModelSerializer):
    """Serializer for Surah model."""

    class Meta:
        model = Surah
        fields = '__all__'


class AyahSerializer(serializers.ModelSerializer):
    """Serializer for Ayah model."""

    class Meta:
        model = Ayah
        fields = ('number', 'text')


class SurahDetailsSerializer(serializers.ModelSerializer):
    """Serializer for detailed Sura detailed."""

    ayahs = AyahSerializer(many=True, read_only=True)

    class Meta:
        model = Surah
        fields = '__all__'
