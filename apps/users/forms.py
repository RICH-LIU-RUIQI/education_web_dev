from django import forms
from captcha.fields import CaptchaField

from apps.users.models import UserProfile


class LoginForm(forms.Form):
    # object must have same name as the object in Request
    username = forms.CharField(required=True, min_length=3)
    password = forms.CharField(required=True, min_length=4)
    sms_code = forms.CharField(max_length=5, min_length=5)
    # captcha = CaptchaField()


class DynamicLoginForm(forms.Form):
    captcha = CaptchaField()
    # mobile = forms.CharField(required=True, min_length=5)


class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=3)
    password = forms.CharField(required=True)

    # put mobile check in form
    def clean_mobile(self):
        mobile_input = self.data.get('mobile')
        user = UserProfile.objects.filter(mobile=mobile_input)
        if user:
            raise forms.ValidationError('Number is already registered')
        else:
            return mobile_input




