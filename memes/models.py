from django.db import models
from django.shortcuts import get_object_or_404

from functools import total_ordering
import hashlib

# Create your models here.

@total_ordering
class Meme(models.Model):

    image = models.ImageField(upload_to="memes_storage/%Y/%m/%d")
    uploader = models.ForeignKey('users.User', on_delete=models.CASCADE)
    image_hash = models.CharField(max_length=200)

    def __str__(self):
        return f"Meme #{self.id}: by {self.uploader}"

    def __eq__(self, other):
        return self.id == other.id

    def __gt__(self,other):
        return self.id > other.id

    def __hash__(self):
        return super(Meme, self).__hash__()

    def get_score(self):
        my_likes = Likes.objects.filter(models.Q(first_meme__id=self.id)|models.Q(second_meme__id=self.id))
        score = 0
        for like in my_likes:
            score += (like.get_score(self.id))
        return score

    def get_hash(self):
        BUFFER_SIZE = 65536
        md5 = hashlib.md5()
        f =  self.image.open()
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            md5.update(data)
        f.seek(0)
        return md5.hexdigest()

    def save(self, **kwargs):
        image_hash = self.get_hash()
        # TODO: Remove duplicate values iin db  now
        if not Meme.objects.filter(image_hash=image_hash):
            self.image_hash = image_hash
            super().save(**kwargs)

class Likes(models.Model):

    hash = models.CharField(max_length=64)
    first_meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='first_meme')
    second_meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='second_meme')
    first_meme_likes = models.IntegerField(default=0)
    second_meme_likes = models.IntegerField(default=0)

    @staticmethod
    def get_likes_object(meme_1, meme_2):
        # TODO: Check if meme_1 & meme_2 are of type meme
        meme_1, meme_2 = min(meme_1,meme_2), max(meme_1,meme_2)
        hash_string = f"{meme_1.id}-{meme_2.id}"
        _hash = hashlib.md5(hash_string.encode())
        
        try:
            _object = Likes.objects.get(hash=_hash.hexdigest())
        except:
            _object = None
        finally:
            return _object

    @staticmethod
    def add_new_combo(meme_1, meme_2):
        meme_1, meme_2 = min(meme_1,meme_2), max(meme_1,meme_2)
        hash_string = f"{meme_1.id}-{meme_2.id}"
        _hash = hashlib.md5(hash_string.encode())

        new_likes_obj = Likes(hash=_hash.hexdigest(), first_meme=meme_1, second_meme=meme_2)
        new_likes_obj.save()

        return new_likes_obj

    def get_likes(self):
        return self.first_meme_likes, self.second_meme_likes, self.first_meme_likes + self.second_meme_likes

    def get_score(self, meme_id):
        # TODO: Add tests here
        fl, sl, tl = self.get_likes()
        if meme_id == self.first_meme.id:
            return fl/float(tl)
        return sl/float(tl)
        
    def __str__(self):
        return f"Likes data with hash {self.hash}"
