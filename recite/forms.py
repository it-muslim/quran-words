from django import forms
from .models import Reciter


class ReciteForm(forms.BaseModelForm):
    """Recitation model form"""

    url_mask = forms.CharField(max_length=200)
    segments_file = forms.FileField()

    def save(self, commit=True):
        segments_file = self.cleaned_data.get('segments_file', None)
        url_mask = self.cleaned_data.get('url_mask', None)

        # ...do something with extra_field here...
        return super(ReciteForm, self).save(commit=commit)

    class Meta:
        model = Reciter
        fields = '__all__'
