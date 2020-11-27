from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from quran.api import views as quran_views
from recite.api import views as recite_views
from django.views.generic import TemplateView

router = routers.SimpleRouter()
router.register(
    r'surahs', quran_views.SurahListRetrieveView, basename="surah")
router.register(
    r'reciters', recite_views.ReciterListRetrieveView, basename="reciter")
router.register(
    r'recitations', recite_views.RecitationListRetrieveView,
    basename="recitation")


urlpatterns = [
    path('openapi', get_schema_view(
        title="Quran API",
        patterns=[
            path('api/', include(router.urls)),
        ]
    ), name='openapi-schema'),

    path('api/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

    path('admin/', admin.site.urls),

    url('api/', include((router.urls, 'api'), namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
