from .login_required import LoginRequiredView
from django.shortcuts import render, redirect


class IndexView(LoginRequiredView):
    def get(self, request):
        return render(request, 'wg_manager/index.html', context=None)
