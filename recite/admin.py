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
    """Reciter Form has additional segments_file field of Recitations model"""
    segments_file = forms.FileField()
    audio_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

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

        segments_file = form.cleaned_data['segments_file'].file
        csv_content = self.handle_csv_data(
            segments_file, encoding=request.encoding)

        files = request.FILES.getlist('audio_files')

        for row in csv_content:
            segments_list = json.loads(row.get("segments"))
            segments = ",".join(
                (f"{segment[2]}:{segment[3]}" for segment in segments_list)
            )

            ayah = self.get_ayah_object_from_row(row)
            file_ayah = self.get_file_audio(files, ayah)

            recitation, _ = Recitation.objects.get_or_create(
                ayah=ayah,
                reciter=obj,
                segments=segments,
                audio=file_ayah
            )

    def get_ayah_object_from_row(self, row):
        """Getting Ayah object for Recitation from csv file row"""
        ayah_id = row.get('ayat')
        surah_id = row.get('sura')

        ayah = Ayah.objects.get(
            number=ayah_id,
            surah=surah_id,
        )
        return ayah

    def get_file_audio(self, files, ayah):
        """Loop through uploading files and find corresponding ayah"""
        file_ayah = None
        for file_mp3 in files:
            if str(ayah) + '.mp3' == str(file_mp3):
                file_ayah = file_mp3
                break

        if not file_ayah:
            raise ValueError(
                f"Not found Recitation audio file for ayah {ayah}")

        return file_ayah

    def handle_csv_data(self, segments_file, encoding):
        """Return csv file as ordered dict"""
        segments_file = io.TextIOWrapper(segments_file, encoding=encoding)
        segments_file.seek(0)
        reader = csv.DictReader(segments_file)
        reader = sorted(reader, key=lambda x: int(x['sura']))

        return reader
