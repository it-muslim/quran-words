# -*- coding: utf-8 -*-
'''Routes for api'''
from rest_framework import routers
from surah.viewsets import SurahViewSet

router = routers.DefaultRouter()
router.register(r'surah', SurahViewSet)
