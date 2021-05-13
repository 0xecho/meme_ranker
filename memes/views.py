from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class RankMemesView(TemplateView):
	template_name = "rank.html"