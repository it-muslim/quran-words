from rest_framework import serializers

from .models import Ayah, Surah


class SurahSerializer(serializers.ModelSerializer):
    '''Serializer for Surah model'''
    class Meta:
        model = Surah
        fields = '__all__'


class AyahSerializer(serializers.ModelSerializer):
    '''Serializer for Ayah model'''
    class Meta:
        model = Ayah
        fields = ('number', 'text')


class SurahDetailsSerializer(serializers.ModelSerializer):
    '''
    Serializer for Surah details which
    include Surah information and its Ayahs
    '''
    ayahs = AyahSerializer(many=True, read_only=True)

    class Meta:
        model = Surah
        fields = '__all__'
