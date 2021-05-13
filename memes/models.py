from django.db import models
from django.shortcuts import get_object_or_404

from functools import total_ordering
import hashlib

# Create your models here.

@total_ordering
class Meme(models.Model):

	image = models.FileField(upload_to="memes/%Y/%m/%d")
	uploader = models.CharField(default="oxecho", max_length=200, blank=True)

	def __str__(self):
		return f"Meme #{self.id}: by {self.uploader}"

	def __eq__(self, other):
		return self.id == other.id

	def __gt__(self,other):
		return self.id > other.id

class Likes(models.Model):

	hash = models.CharField(max_length=64)	
	first_meme_likes = models.IntegerField()
	second_meme_likes = models.IntegerField()

	@staticmethod
	def get_likes_object(meme_1, meme_2):
		# TODO: Check if meme_1 & meme_2 are of type meme
		meme_1, meme_2 = min(meme_1,meme_2), max(meme_1,meme_2)
		hash_string = f"{meme_1.id}-{meme_2.id}"
		_hash = hashlib.md5(hash_string.encode())
		try:
			_object = Likes.objects.get(hash=_hash.digest())
		except:
			_object = None
		finally:
			return _object

	def get_likes(self):
		return self.first_meme_likes, self.second_meme_likes, sum(self.first_meme_likes, self.second_meme_likes)

	def __str__(self):
		return f"Likes data with hash {self.hash}"
