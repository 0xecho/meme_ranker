from django.forms import ModelForm, fields
from .models import User

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'about', 'profile_picture')