'''Quran app api url endpoints'''
from django.urls import path

from . import views

urlpatterns = [
    path(
        'api/quran/surah/<int:number>/',
        views.SurahDetailsView.as_view(),
        name="surah-details"
    ),
    path(
        'api/quran/surah/',
        views.SurahListView.as_view(),
        name="surahs-list",
    )
]
