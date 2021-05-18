from django.urls import path, include
from .views import RankMemesView, TopMemesView, UploadMemesView, get_two_memes, like_meme, ApprovalView

urlpatterns = [
    path('rank/',RankMemesView.as_view(), name='rank'),
    path('approve/',ApprovalView.as_view(), name='approve'),
    path('top/',TopMemesView.as_view(), name='top'),
    path('upload/',UploadMemesView.as_view(), name='upload'),
    path('get_two_memes/',get_two_memes, name='get_two_memes'),
    path('like_meme/',like_meme, name='like_meme'),
]
