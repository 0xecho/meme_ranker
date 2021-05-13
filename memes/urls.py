from django.urls import path, include
from .views import RankMemesView

urlpatterns = [
    path('rank/',RankMemesView.as_view(), name='rank')
]
