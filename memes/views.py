from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.http import JsonResponse

from .models import Meme, Likes
from random import choice
# Create your views here.

class RankMemesView(TemplateView):
	template_name = "rank.html"

class TopMemesView(DetailView):
	model = Meme

def get_two_memes(request):
	meme_ids = Meme.objects.values_list('id', flat=True)

	if len(meme_ids)<2:
		return JsonResponse(data={"message":"Internal Error"}, status=500)

	meme_1_id = choice(meme_ids)
	meme_2_id = choice(meme_ids)
	while meme_2_id == meme_1_id:
		meme_2_id = choice(meme_ids)

	meme_1 = Meme.objects.get(id=meme_1_id)
	meme_2 = Meme.objects.get(id=meme_2_id)
	respose_data = {
		"meme_urls": [meme_1.image.url, meme_2.image.url]
	}

	return JsonResponse(data=respose_data)

def like_meme(request):
	return JsonResponse(data={"Nothing":"DEAR"})

