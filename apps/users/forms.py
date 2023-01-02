from django import forms


class LoginForm(forms.Form):
    # object must have same name as the object in Request
    username = forms.CharField(required=True, min_length=3)
    password = forms.CharField(required=True, min_length=4)


