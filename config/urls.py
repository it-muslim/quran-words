from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include

from quran.api import views as quran_views

router = routers.SimpleRouter()
router.register(r'quran/surah', quran_views.SurahListRetrieveView)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include((router.urls, 'api'), namespace='api')),
]
