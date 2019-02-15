'''Quran app api url endpoints'''
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r'quran/(?P<surah_id>\d+)/$',
        views.SurahDetailsView.as_view(),
        name="surah-details"
    ),
    re_path(
        r'quran/$',
        views.SurahListView.as_view(),
        name="surahs-all",
    )
]
