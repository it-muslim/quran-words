from django.contrib import admin

from .forms import ReciteForm
from .models import Reciter, Recitation


admin.site.register(Reciter)
admin.site.register(Recitation)
