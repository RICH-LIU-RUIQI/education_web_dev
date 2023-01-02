from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.users.forms import LoginForm


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]

            user = authenticate(user_name=user_name, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
            else:
                return render(request, 'login.html', {'msg': 'incorrect username or password', 'login_form': login_form})
        else:
            # user not found
            return render(request, 'login.html', {'login_form': login_form})
