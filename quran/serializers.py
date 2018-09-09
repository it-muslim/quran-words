# -*- coding: utf-8 -*-
'''Serializers for native Python datatypes that can then
be easily rendered to JSON XML or other content types '''

from rest_framework import serializers
from .models import Surah, Ayah


class AyahSerializer(serializers.ModelSerializer):
    '''Serializer for Ayahs'''
    class Meta:
        model = Ayah
        fields = '__all__'


class SurahSerializer(serializers.ModelSerializer):
    '''Serializer for Surah'''
    ayahs = AyahSerializer(many=True, read_only=True)

    class Meta:
        model = Surah
        fields = ('surah_id', 'surah_name', 'surah_ayah_count', 'ayahs')
