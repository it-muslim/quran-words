import csv
import io
import json

from django import forms
from django.contrib import admin

from quran.models import Ayah

from .models import Recitation, Reciter


class RecitationInline(admin.TabularInline):
    """Inline tab of Recitations in admin page of Reciter"""
    # Hide editing of single Recitation field
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    model = Recitation


class ReciterForm(forms.ModelForm):
    """Reciter Form has additional csv_file field of Recitations model"""
    csv_file = forms.FileField()

    class Meta:
        model = Reciter
        fields = '__all__'


@admin.register(Reciter)
class ReciterAdmin(admin.ModelAdmin):
    """Reciter admin page including Recitations"""
    inlines = [
        RecitationInline,
    ]
    form = ReciterForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        csv_file = form.cleaned_data['csv_file'].file
        csv_content = self.handle_csv_data(csv_file, encoding=request.encoding)
        csv_content = sorted(csv_content, key=lambda x: int(x['sura']))

        for row in csv_content:
            segments_list = json.loads(row.get("segments"))
            segments = ",".join(
                (f"{segment[2]}:{segment[3]}" for segment in segments_list)
            )

            ayah_id = row.get("ayat")
            surah_id = row.get("sura")

            ayah = Ayah.objects.get(
                number=ayah_id,
                surah=surah_id,
            )

            recitation, _ = Recitation.objects.get_or_create(
                ayah=ayah,
                reciter=obj,
                segments=segments,
            )

    def handle_csv_data(self, csv_file, encoding):
        """Return csv file as ordered dict"""
        csv_file = io.TextIOWrapper(csv_file, encoding=encoding)
        csv_file.seek(0)
        reader = csv.DictReader(csv_file)
        return reader
