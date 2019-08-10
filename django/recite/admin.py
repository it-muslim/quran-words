import csv
import io
import json
import os
import tempfile
from collections import defaultdict
from zipfile import ZipFile

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.conf import settings
from django.forms import BaseInlineFormSet

from quran.models import Surah, Ayah

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
    audio_zip_file = forms.FileField(required=False)
    audio_external_pattern = forms.URLField(
        required=False, widget=forms.URLInput(attrs={'size': 80}),
        help_text="For example: http://example.com/{surah}{ayah}.mp3 <br> {surah} and {ayah} required")

    def clean(self):
        cleaned_data = super().clean()
        audio_zip_field = cleaned_data.get("audio_zip_file")
        pattern = cleaned_data.get("audio_external_pattern")

        if not audio_zip_field and (not pattern or "{surah}" not in pattern or "{ayah}" not in pattern):
            raise forms.ValidationError(
                "Please provide audio zip file or proper external audio url pattern."
            )

    class Meta:
        model = Reciter
        fields = '__all__'


@admin.register(Reciter)
class ReciterAdmin(admin.ModelAdmin):
    """
    Reciter admin page including Recitations.

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
        csv_content_list = self.get_csv_list(request.encoding, segments_file)
        segments_dict = self.get_segments_dict(csv_content_list)
        slug = form.cleaned_data['slug']

        audio_zip_file = form.cleaned_data.get('audio_zip_file')
        pattern_field = form.cleaned_data.get('audio_external_pattern')

        # Unzip or link audio files for recitations
        file_links = None
        if audio_zip_file:
            file_links = self.get_file_links_dict(audio_zip_file, slug, segments_dict)
        else:
            file_links = self.create_external_file_links_dict(pattern_field, segments_dict)

        self.check_segments_has_files(segments_dict, file_links)

        # Create recitations from segments and file_links
        for surah_number, ayahs in segments_dict.items():
            for ayah_number, segments in ayahs.items():

                audio_link = file_links[surah_number][ayah_number]

                surah = Surah.objects.get(
                    number=surah_number
                )
                ayah = Ayah.objects.get(
                    number=ayah_number,
                    surah=surah_number,
                )
                Recitation.objects.get_or_create(
                    surah=surah,
                    ayah=ayah,
                    reciter=obj,
                    segments=segments,
                    audio=audio_link
                )

    @staticmethod
    def create_external_file_links_dict(pattern_field, segments_dict):
        """Create paths for external sources provided in pattern field."""
        file_links = defaultdict(lambda: defaultdict(int))

        for surah_number, ayahs in segments_dict.items():
            for ayah_number, _segments in ayahs.items():
                surah = f"{surah_number:03d}"
                ayah = f"{ayah_number:03d}"

                formed_link = pattern_field.replace("{surah}", surah).replace("{ayah}", ayah)
                file_links[surah_number][ayah_number] = formed_link

        return file_links

    @staticmethod
    def check_segments_has_files(segments_dict, file_links):
        """Check if each segments row has corresponding audio file"""
        not_found_files_for_segments = []

        if not file_links:
            raise ValidationError(message="No audio files provided")

        for surah_number, ayahs in segments_dict.items():
            for ayah_number, segments in ayahs.items():
                if not file_links[surah_number][ayah_number]:
                    not_found_files_for_segments.append(
                        f"{surah_number:03d}{ayah_number:03d}.mp3")
        if not_found_files_for_segments:
            raise ValidationError(
                message="No audio files "
                f"{', '.join(not_found_files_for_segments)} found",
            )

    @staticmethod
    def get_file_links_dict(audio_zip_file, slug, segments_dict):
        """
        Process audio zip file uploaded and create dict
        :return: file_links[surah][ayah] = file_link
        """
        # Create directories for surahs
        recitation_dir = os.path.join(settings.MEDIA_ROOT, 'recite', str(slug))
        for surah, _ayah in segments_dict.items():
            surah_dir = os.path.join(recitation_dir, f"{surah:03d}")
            if not os.path.exists(surah_dir):
                os.makedirs(surah_dir)

        file_links = defaultdict(lambda: defaultdict(int))

        with tempfile.TemporaryDirectory(dir=recitation_dir) as temp_dir:
            # Extract zipped audio files to a temp directory
            audio_files = ZipFile(audio_zip_file, 'r')
            audio_files.extractall(temp_dir)

            # let's create dict file_paths[surah][ayah] = file_path
            for root, _directories, files in os.walk(temp_dir):
                for filename in files:
                    if filename.endswith('.mp3'):
                        # extract surah and ayah number from filename
                        surah_str = filename[:3]
                        ayah_str = filename[3:6]
                        try:
                            surah_number = int(surah_str)
                            ayah_number = int(ayah_str)
                        except ValueError:
                            print(f"Not normal format mp3 file {filename} ignored")
                        else:
                            temp_filepath = os.path.join(os.path.abspath(root), filename)
                            formed_filepath = os.path.join(recitation_dir, filename[:3], filename[3:])
                            # move temp file to folder
                            os.link(temp_filepath, formed_filepath)
                            # create link for file
                            file_link = f"recite/{slug}/{filename[:3]}/{filename[3:]}"
                            file_links[surah_number][ayah_number] = file_link
        return file_links

    @staticmethod
    def get_csv_list(encoding, segments_file):
        """
        Process csv file uploaded and return
        csv content as list of OrderedDicts
        """
        segments_file = io.TextIOWrapper(
            segments_file, encoding=encoding)
        segments_file.seek(0)
        csv_content_dict = csv.DictReader(segments_file)
        csv_content_sorted = list(sorted(
            csv_content_dict, key=lambda x: int(x['sura'])))

        return csv_content_sorted

    @staticmethod
    def get_segments_dict(csv_content_sorted):
        """
        Process sorted csv dict and return dict
        segments_dict[surah][ayah] = [segments]
        """
        segments_dict = defaultdict(lambda: defaultdict(list))

        for row in csv_content_sorted:
            segments_list = json.loads(row.get("segments"))
            segments_string = ",".join(
                (f"{segment[2]}:{segment[3]}" for segment in segments_list)
            )
            surah_str = row.get('sura')
            ayah_str = row.get('ayat')
            try:
                surah_number = int(surah_str)
                ayah_number = int(ayah_str)
            except ValueError:
                print(f"Not normal format for csv at row {row} ignored")
            else:
                segments_dict[surah_number][ayah_number] = segments_string
        return segments_dict
