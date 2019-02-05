from django.contrib import admin

from .forms import ReciteForm
from .models import Reciter


class ReciterAdmin(admin.ModelAdmin):
    form = ReciteForm


admin.site.register(Reciter, ReciterAdmin)
