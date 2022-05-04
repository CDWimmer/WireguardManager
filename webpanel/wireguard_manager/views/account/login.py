from django import views, forms
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


class LoginForm(forms.Form):
    template_name = "wg_manager/forms/login_form.html"
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class LoginView(views.View):
    def get(self, request):
        return render(request, 'wg_manager/account/login.html', context={'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, 'wg_manager/account/login.html', context={'form': form})
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is None:
            form.add_error(None, "Username or password is incorrect")
            return render(request, 'wg_manager/account/login.html', context={'form': form})
        login(request, user)
        return redirect(request.GET.get('after', '/'))
