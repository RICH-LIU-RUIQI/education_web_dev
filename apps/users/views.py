from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from io import BytesIO


from apps.users.models import UserProfile
from apps.users.forms import LoginForm, DynamicLoginForm, RegisterGetForm, RegisterPostForm
from apps.users.utils import sms_produce


class RegisterView(View):
    def get(self, request):
        # login_form = LoginForm()
        register_get_form = RegisterGetForm()
        return render(request, 'register.html', {'register_get_form': register_get_form})

    def post(self, request):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            # creat a new user
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            # back 2 register page
            register_get_form = RegisterGetForm()
            return render(request, 'register.html', {'register_get_form': register_get_form,
                                                     'register_post_form': register_post_form})


class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        if send_sms_form.is_valid():
            pass
        else:
            pass


class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        # image captcha
        login_form = LoginForm()
        next = request.GET.get('next', '')  # get the latest url before login
        return render(request, 'login.html', {'login_form': login_form,
                                              'next': next})

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            sms_code = login_form.cleaned_data['sms_code']
            true_sms = request.session.get('image_code', "")
            if sms_code.upper() != true_sms.upper():
                return render(request, 'login.html', {'msg': 'Incorrect SMS', 'login_form': login_form})
            user = UserProfile.objects.get(username=user_name)
            if not user:
                return render(request, 'login.html',
                              {'msg': 'Incorrect Username', 'login_form': login_form})
            pwd = user.password
            if check_password(password, pwd):
                login(request, user)
                next = request.GET.get('next', '')  # get the latest url before login
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("home"))
            else:
                return render(request, 'login.html',
                              {'msg': 'incorrect password', 'login_form': login_form})
        else:
            # user not found
            return render(request, 'login.html', {'login_form': login_form})


def image_sms(request):
    """ Produce Image SMS code """
    # 调用pillow函数，生成图片
    img, code_string = sms_produce.check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(6000)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
