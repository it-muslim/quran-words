from django.urls import path

from . import views

app_name = 'quran'

urlpatterns = [
    path('', views.home, name='home'),
    path('recitation/add/', views.add_recitation, name="add-recitation")
]
