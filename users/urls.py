from django.urls import path, include
from .views import SigninPageView, SignupPageView, ProfilePageView, EditProfilePageView

urlpatterns = [
    path('signin/', SigninPageView.as_view(), name='signin'),
    path('redirect/', SigninPageView.redirect, name='telegram_redirect'),
    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('profile/edit', EditProfilePageView.as_view(), name='edit_profile'),
    path('signup/', SignupPageView.as_view(), name='signup'),
]
