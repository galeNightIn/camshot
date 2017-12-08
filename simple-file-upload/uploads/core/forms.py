from django import forms

from uploads.core.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)