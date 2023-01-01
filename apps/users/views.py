from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.urls import reverse


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        user_name = request.POST.get('username', "")
        pwd = request.POST.get('password', "")
        user = authenticate(user_name=user_name, password=pwd)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            # user not found
            return render(request, 'login.html', {'msg': 'User is not found or incorrect passwrod'})
