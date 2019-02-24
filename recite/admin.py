import csv
import io
import json
import os
import tempfile
from collections import defaultdict
from zipfile import ZipFile

from django import forms
from django.contrib import admin
from django.core.files import File
from django.forms import BaseInlineFormSet

from quran.models import Ayah

from .models import Recitation, Reciter


class RecitationFormSet(BaseInlineFormSet):
    """FormSet for Recitation shows limited value of Recitations"""

    def get_queryset(self):
        qs = super(RecitationFormSet, self).get_queryset()
        return qs[:10]


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
    formset = RecitationFormSet


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

    def has_change_permission(self, request, obj=None):
        return False

    inlines = [
        RecitationInline,
    ]
    form = ReciterForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Create a dict segments_dict[surah][ayah] = segments
        segments_file = form.cleaned_data['segments_file'].file
        segments_dict = self.get_segments_dict(request.encoding, segments_file)

        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract zipped audio files to temp directory
            audio_zip_file = form.cleaned_data['audio_zip_file']
            audio_files = ZipFile(audio_zip_file, 'r')

            audio_files.extractall(temp_dir)

            # let's create dict file_paths[surah][ayah] = file_path
            file_paths = self.get_file_paths_dict(temp_dir=temp_dir)
            # let's create Recitations from segments and file_paths
            for surah_number, ayahs in segments_dict.items():
                for ayah_number, segments in ayahs.items():
                    with open(file_paths[surah_number][ayah_number], 'rb')\
                            as audio_file:

                        file_ayah = File(audio_file)
                        ayah = Ayah.objects.get(
                            number=ayah_number,
                            surah=surah_number,
                        )

                        Recitation.objects.get_or_create(
                            ayah=ayah,
                            reciter=obj,
                            segments=segments,
                            audio=file_ayah
                        )

    def get_file_paths_dict(self, temp_dir):
        """
        Process audio zip file uploaded and create dict
        :return: file_paths[surah][ayah] = file_path
        """
        file_paths = defaultdict(lambda: defaultdict(int))

        for root, _directories, files in os.walk(temp_dir):
            for filename in files:
                if filename.endswith('.mp3'):
                    filepath = os.path.join(root, filename)

                    # extract surah and ayah number from filename
                    surah_str = filename[:3]
                    ayah_str = filename[3:6]
                    try:
                        surah_number = int(surah_str)
                        ayah_number = int(ayah_str)
                    except ValueError:
                        print(f"Not normal format mp3 file {filename}")
                    file_paths[surah_number][ayah_number] = filepath

        return file_paths

    def get_segments_dict(self, encoding, segments_file):
        """
        Process csv file uploaded and return dict
        segments_dict[surah][ayah] = [segments]
        """

        segments_dict = defaultdict(lambda: defaultdict(list))

        segments_file = io.TextIOWrapper(
            segments_file, encoding=encoding)
        segments_file.seek(0)
        csv_content_dict = csv.DictReader(segments_file)
        csv_content_sorted = sorted(
            csv_content_dict, key=lambda x: int(x['sura']))

        for row in csv_content_sorted:
            segments_list = json.loads(row.get("segments"))
            segments = ",".join(
                (f"{segment[2]}:{segment[3]}" for segment in segments_list)
            )

            surah_str = row.get('sura')
            ayah_str = row.get('ayat')
            try:
                surah_number = int(surah_str)
                ayah_number = int(ayah_str)
            except ValueError:
                print(f"Not normal format for csv at row {row}")

            segments_dict[surah_number][ayah_number] = segments

        return segments_dict
