# -*- coding: utf-8 -*-
'''Serializers for native Python datatypes that can then
be easily rendered to JSON XML or other content types '''

from rest_framework import serializers
from .models import Surah


class SurahSerializer(serializers.ModelSerializer):
    '''Serializer for Surah'''
    class Meta:
        model = Surah
        fields = '__all__'
