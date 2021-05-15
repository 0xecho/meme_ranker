from django.forms.models import ModelForm
from django.forms import fields
from django import forms

from .models import Meme

class MemeUploadForm(ModelForm):
	image = fields.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
	class Meta:
		model = Meme
		fields = ('image',)