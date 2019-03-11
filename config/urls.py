from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from quran.api import views as quran_views

router = routers.SimpleRouter()
router.register(
    r'quran/surah', quran_views.SurahListRetrieveView, base_name="quran")

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/', include((router.urls, 'api'), namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
