from django import forms


class RecitationForm(forms.Form):
    """Recitation model form"""

    reciter_name = forms.CharField(
        label="Name of the reciter", max_length=100
    )
    bitrate = forms.IntegerField(
        label="Bitrate", required=False, help_text="Bitrate of an audio file"
    )
    style = forms.CharField(
        label="Style",
        max_length=20,
        required=False,
        help_text="Qur'an reading style",
    )
    url_mask = forms.CharField(max_length=200)
    segments_file = forms.FileField()
