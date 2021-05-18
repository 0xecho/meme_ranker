from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

	username = models.CharField(max_length=100, blank=False, null=False, unique=True)
	first_name = models.CharField(max_length=100, default="")
	last_name = models.CharField(max_length=100, default="")
	about = models.CharField(max_length=500)
	profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True, default='profile_pictures/default.jpg')

	show_telegram_username = models.BooleanField(default=False)
	telegram_id = models.CharField(max_length=100)
	telegram_username = models.CharField(max_length=100)
	telegram_name = models.CharField(max_length=100)

	@property
	def image_url(self):
		if self.profile_picture:
			return self.profile_picture.url
		return 'profile_picture/default.jpg'
