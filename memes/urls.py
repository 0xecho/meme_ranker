from django.urls import path, include
from .views import RankMemesView, TopMemesView, get_two_memes, like_meme

urlpatterns = [
    path('rank/',RankMemesView.as_view(), name='rank'),
    path('top/',TopMemesView.as_view(), name='top'),
    path('get_two_memes/',get_two_memes, name='get_two_memes'),
    path('like_meme/',like_meme, name='like_meme'),
]
