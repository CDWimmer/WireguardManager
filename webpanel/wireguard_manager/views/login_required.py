from django import views
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredView(LoginRequiredMixin, views.View):
    login_url = '/account/login/'
    redirect_field_name = 'after'
