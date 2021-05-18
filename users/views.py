from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth import login
from django.contrib.auth import logout as _logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import UserForm
from .models import User

import hmac
import hashlib
import time
# Create your views here.

ONE_DAY_IN_SECONDS = 86400

def verify_telegram_authentication(request_data):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    request_data = request_data.copy()

    received_hash = request_data['hash']
    auth_date = request_data['auth_date']

    request_data.pop('hash', None)
    request_data_alphabetical_order = sorted(request_data.items(), key=lambda x: x[0])

    data_check_string = []

    for data_pair in request_data_alphabetical_order:
        key, value = data_pair[0], data_pair[1]
        data_check_string.append(key + '=' + value)

    data_check_string = '\n'.join(data_check_string)

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    _hash = hmac.new(secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

    unix_time_now = int(time.time())
    unix_time_auth_date = int(auth_date)

    if unix_time_now - unix_time_auth_date > ONE_DAY_IN_SECONDS:
        return None # TODO: Return message saying old data

    if _hash != received_hash:
        return None # TODO: Return message saying invalid data

    return request_data

class SigninPageView(TemplateView):
    template_name = "users/signin.html"
    extra_context = {
        "REDIRECT_URL": settings.TELEGRAM_LOGIN_REDIRECT_URL
    }

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('rank')
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def redirect(request):
        valid_data = verify_telegram_authentication(request.GET)
        if valid_data:
            user = User.objects.filter(telegram_id=valid_data.get('id', -1))
            if not user.count():
                request.session['id'] = valid_data.get('id', -1)
                request.session['tg_username'] = valid_data.get('username', -1)
                return redirect('signup')
            else:
                ret = login(request, user[0])
        else:
            # TODO: redirect('error')
            pass
        return redirect('rank')

class SignupPageView(CreateView):
    form_class = UserForm
    template_name = "users/signup.html"
    success_url = reverse_lazy('rank')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.session.get('id') or not self.request.session.get('tg_username'):
            return redirect('rank')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if not self.request.session.get('id') or not self.request.session.get('tg_username'):
            return self.form_invalid(form)

        ret = super().form_valid(form)
        self.object.telegram_id = self.request.session.get('id')
        self.object.telegram_username = self.request.session.get('tg_username')
        self.object.telegram_name = self.request.session.get('tg_username')
        self.object.save()

        del self.request.session['id']
        del self.request.session['tg_username']

        login(request, self.object)

        return ret

@method_decorator(login_required(login_url=reverse_lazy("signin")), name='dispatch')
class ProfilePageView(TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        new_context = {
            'object': self.request.user,
        }
        kwargs.update(new_context)
        return kwargs

@method_decorator(login_required(login_url="signin"), name='dispatch')
class EditProfilePageView(UpdateView):
    template_name = "users/edit_profile.html"
    form_class = UserForm
    success_url = reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        new_context = {
            'object': self.request.user,
        }
        kwargs.update(new_context)
        return kwargs        

    def get_initial(self):
        new_initial_data = {
            "username": self.request.user.username,
            "first_name": self.request.user.first_name,
            "last_name": self.request.user.last_name,
            "about": self.request.user.about,
        }
        self.initial.update(new_initial_data)

        return super().get_initial()

    def get_object(self):
        return self.request.user

def logout(request):
    _logout(request)
    return redirect("rank")
