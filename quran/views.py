import io
import csv
import json
import urllib.request
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from .forms import RecitationForm
from .models import Ayah, Reciter, Recitation


class QuranURLopener(urllib.request.URLopener):
    """class to access permissions for downloading audio ayahs"""

    version = "Mozilla/5.0"


def handle_csv_data(csv_file, encoding):
    """return csv file as ordered dict"""
    csv_file = io.TextIOWrapper(csv_file, encoding=encoding)
    csv_file.seek(0)
    reader = csv.DictReader(csv_file)
    return reader


def get_audio_link(url_mask, surah_number, ayah_number):
    """
    generate link for audio ayah from url mask
    url_mask: https://example.com/{sura}{ayat}.mp3
    surah_number: 1-114
    ayah_number: 1-6236
    """
    surah = str(surah_number).zfill(3)
    ayah = str(ayah_number).zfill(3)
    return url_mask.format(sura=surah, ayat=ayah)


def home(request):
    return render(request, "quran/index.html")


def add_recitation(request):
    if request.method == "POST" and request.FILES:
        form = RecitationForm(request.POST, request.FILES)
        if form.is_valid():
            # get or create new reciter
            reciter_name = form.cleaned_data["reciter_name"]
            bitrate = form.cleaned_data["bitrate"]
            style = form.cleaned_data["style"]
            reciter, created = Reciter.objects.get_or_create(
                name=reciter_name, bitrate=bitrate, style=style
            )
            # get url_mask
            url_mask = form.cleaned_data["url_mask"]
            # get segments
            csv_file = form.cleaned_data["segments_file"].file
            csv_content = handle_csv_data(csv_file, encoding=request.encoding)
            for row in csv_content:
                segments_list = json.loads(row.get("segments"))
                segments = ",".join(
                    (f"{segment[2]}:{segment[3]}" for segment in segments_list)
                )
                ayah_id = row.get("ayat_id")
                ayah = Ayah.objects.get(pk=ayah_id)
                # generate link for audio file
                audio_link = get_audio_link(
                    url_mask, ayah.surah.number, ayah.number
                )
                # opener audio ayahs
                downloader = QuranURLopener()
                # get audio file and create Recitation object
                with NamedTemporaryFile(
                    suffix=".mp3", delete=True
                ) as temp_file:
                    audio_file = downloader.open(audio_link)
                    temp_file.write(audio_file.read())
                    temp_file.flush()
                    rec = Recitation.objects.create(
                        ayah=ayah,
                        segments=segments,
                        reciter=reciter,
                        audio=File(temp_file),
                    )
                    rec.save()
                    print(rec, rec.audio)

            return HttpResponseRedirect("/")

    else:
        form = RecitationForm()

    return render(request, "quran/add_recitation.html", {"form": form})
