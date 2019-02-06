from django import forms
from django.contrib import admin

from .models import Reciter, Recitation


class ReciterForm(forms.ModelForm):
    class Meta:
        model = Reciter
        fields = '__all__'


class RecitationForm(forms.ModelForm):
    class Meta:
        model = Recitation
        exclude = ('ayah', 'segments')


class RecitationInline(admin.TabularInline):
    model = Recitation
    form = RecitationForm


@admin.register(Reciter)
class ReciterAdmin(admin.ModelAdmin):
    inlines = [
        RecitationInline,
    ]
