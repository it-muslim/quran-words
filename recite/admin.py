import csv
import io
import json
from zipfile import ZipFile

from django import forms
from django.contrib import admin

from quran.models import Ayah

from .models import Recitation, Reciter
import os
import tempfile
import shutil
from django.core.files import File


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
    audio_zip_file = forms.FileField()

    class Meta:
        model = Reciter
        fields = '__all__'


@admin.register(Reciter)
class ReciterAdmin(admin.ModelAdmin):
    """
    Reciter admin page including Recitations
    Modified save_model method allows to save Recitations
    objects at the same model creation form
    """
    inlines = [
        RecitationInline,
    ]
    form = ReciterForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # process csv file uploaded
        segments_file = form.cleaned_data['segments_file'].file
        csv_content = self.read_segments_csv(
            segments_file, encoding=request.encoding)

        # process audio zip file uploaded
        audio_zip_file = form.cleaned_data['audio_zip_file']
        temp_dir = self.get_unzipped_files_dir(audio_zip_file)
        file_paths = self.get_file_paths(temp_dir)

        # create Recitation objects from processed data
        for row in csv_content:
            segments_list = json.loads(row.get("segments"))
            segments = ",".join(
                (f"{segment[2]}:{segment[3]}" for segment in segments_list)
            )

            ayah = self.get_ayah_object_from_row(row)
            file_ayah_path = self.get_file_audio_path(file_paths, ayah)

            with open(file_ayah_path, 'rb') as f:
                file_ayah = File(f)

                recitation, _ = Recitation.objects.get_or_create(
                    ayah=ayah,
                    reciter=obj,
                    segments=segments,
                    audio=file_ayah
                )

        shutil.rmtree(temp_dir)

    def get_file_paths(self, temp_dir):
        """Return file paths from temp_dir checking subdirectories"""
        file_paths = []
        for root, directories, files in os.walk(temp_dir):
            for filename in files:
                if filename.endswith('.mp3'):
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)

        return file_paths

    def get_ayah_object_from_row(self, row):
        """Getting Ayah object for Recitation from csv file row"""
        ayah_id = row.get('ayat')
        surah_id = row.get('sura')

        ayah = Ayah.objects.get(
            number=ayah_id,
            surah=surah_id,
        )
        return ayah

    def get_file_audio_path(self, file_paths, ayah):
        """Search in uploaded files for corresponding ayah"""

        file_ayah_name_expected = str(ayah) + '.mp3'
        file_ayah = None
        for file_path in file_paths:
            if file_ayah_name_expected == os.path.basename(file_path):
                file_ayah = file_path
                break

        if not file_ayah:
            raise ValueError(
                f"Not found Recitation audio file for ayah {ayah}")

        return file_ayah

    def read_segments_csv(self, segments_file, encoding):
        """Return csv file as ordered dict"""
        segments_file = io.TextIOWrapper(segments_file, encoding=encoding)
        segments_file.seek(0)
        reader = csv.DictReader(segments_file)
        reader = sorted(reader, key=lambda x: int(x['sura']))

        return reader

    def get_unzipped_files_dir(self, audio_zip_file):
        """Return temporary directory of unzipped files"""
        audio_files = ZipFile(audio_zip_file, 'r')

        temp_dir = tempfile.mkdtemp()
        audio_files.extractall(temp_dir)

        return temp_dir
