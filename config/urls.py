from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from quran.api import views as quran_views
from recite.api import views as recite_views


router = routers.SimpleRouter()
router.register(
    r'surahs', quran_views.SurahListRetrieveView, base_name="surah")
router.register(
    r'reciters', recite_views.ReciterListRetrieveView, base_name="reciter")
router.register(
    r'recitations', recite_views.RecitationListRetrieveView,
    base_name="recitation")

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/', include((router.urls, 'api'), namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
