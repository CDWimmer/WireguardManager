from django.urls import path
from .login import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
