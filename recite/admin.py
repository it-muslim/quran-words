from django import forms
from django.contrib import admin

from quran.models import Ayah, Surah

from .models import Recitation, Reciter


class RecitationInline(admin.TabularInline):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    model = Recitation


class ReciterForm(forms.ModelForm):
    csv_file = forms.FileField()

    class Meta:
        model = Reciter
        fields = '__all__'


@admin.register(Reciter)
class ReciterAdmin(admin.ModelAdmin):
    inlines = [
        RecitationInline,
    ]
    form = ReciterForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        csv_file = form.cleaned_data['csv_file']
        recitation, _ = Recitation.objects.get_or_create(
            ayah=Ayah(1, 1),
            reciter=obj,
            segments="3:4,5:7")
