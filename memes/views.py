from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Meme, Likes
from random import choice
import json
# Create your views here.

class RankMemesView(TemplateView):
	template_name = "rank.html"

class TopMemesView(ListView):
	model = Meme
	paginate_by = 10
	template_name = "top.html"

	def get_queryset(self):
		queryset = super().get_queryset()
		for obj in queryset:
			obj.score = obj.get_score()
		return sorted(queryset, key=lambda x:-x.score)

class UploadMemesView(CreateView):
	model = Meme
	fields = ('image', )
	template_name = "upload.html"
	success_url = reverse_lazy("rank")

@require_http_methods(['GET'])
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
	meme_1,meme_2 = min(meme_1, meme_2), max(meme_1, meme_2)

	respose_data = {
		"meme_urls": [meme_1.image.url, meme_2.image.url]
	}

	print(meme_1.get_score())

	request.session["first"] = meme_1_id
	request.session["second"] = meme_2_id

	return JsonResponse(data=respose_data)

@require_http_methods(['POST'])
def like_meme(request):
	request_data = json.loads(request.body.decode())
	choice = str(request_data.get('choice', None))
	
	if not choice or choice not in ['1','2']:
		return JsonResponse(data={"message":"Internal Error"}, status=500)

	meme_1_id = request.session["first"]
	meme_2_id = request.session["second"]

	meme_1 = Meme.objects.get(id=meme_1_id)
	meme_2 = Meme.objects.get(id=meme_2_id)

	likes_obj = Likes.get_likes_object(meme_1, meme_2)
	if not likes_obj:
		likes_obj = Likes.add_new_combo(meme_1, meme_2)

	if choice == '1':
		likes_obj.first_meme_likes += 1 
	else:
		likes_obj.second_meme_likes += 1 

	likes_obj.save()

	return JsonResponse(data={"message":"OK"})

