'''Quran app api url endpoints'''
from django.urls import path

from . import views

urlpatterns = [
    path(
        'api/quran/<int:surah_id>/',
        views.SurahDetailsView.as_view(),
        name="surah-details"
    ),
    path(
        'api/quran/',
        views.SurahListView.as_view(),
        name="surahs-all",
    )
]
