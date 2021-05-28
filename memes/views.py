from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Meme, Likes
from .forms import MemeUploadForm

from random import choice
import json
# Create your views here.

class HomePageView(TemplateView):
	template_name = "home.html"

@method_decorator(login_required(login_url="signin"), name='dispatch')
class RankMemesView(TemplateView):
	template_name = "rank.html"

@method_decorator(login_required(login_url="signin"), name='dispatch')
class TopMemesView(ListView):
	model = Meme
	paginate_by = 10
	template_name = "top.html"

	def get_queryset(self):
		queryset = super().get_queryset()
		for obj in queryset:
			obj.score = obj.get_score()
		all_memes = sorted(queryset, key=lambda x:-x.score)
		rank = 1
		for meme in all_memes:
			meme.rank = rank 
			rank += 1
		return all_memes

@method_decorator(login_required(login_url="signin"), name='dispatch')
class UploadMemesView(CreateView):
	form_class = MemeUploadForm
	template_name = "upload.html"
	success_url = reverse_lazy("rank")

	def form_valid(self, form):
		form.save(commit=False)
		if self.request.FILES:
			for f in self.request.FILES.getlist('image'):
				Meme.objects.create(image=f,uploader=self.request.user)
		return super().form_valid(form)

@require_http_methods(['GET'])
def get_two_memes(request):
	meme_ids = Meme.objects.all().values_list('id', flat=True)
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
@login_required(login_url="signin")
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

@method_decorator(login_required(login_url="signin"), name='dispatch')
class ApprovalView(ListView):
	model = Meme
	template_name = "approval.html"		
	paginate_by = 10
	queryset = Meme.objects.filter(approval='queued')

	
