from django import forms

from .models import Document
from .models import Login


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

class LoginForm(forms.ModelForm):
	class Meta:
		model = Login 
		fields = ('login',)

