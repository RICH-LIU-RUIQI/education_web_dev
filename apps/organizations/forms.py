import re

from django import forms
from apps.operations.models import UserAsk


# class AddAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     mobile = forms.CharField(required=True, max_length=11)
#     course_name = forms.CharField(required=True, max_length=50)


class AddAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        # fields = "__all__"
        # exclude = ['add_time']
        fields = ['name', 'mobile', 'course_name']

    # def clean_mobile(self):
    #     input_mobile = self.cleaned_data['mobile']
    #     regex_input_mobile = '/^1[0-9]$/'
    #     p = re.compile(regex_input_mobile)
    #     if p.match(input_mobile):
    #         return input_mobile
    #     else:
    #         return forms.ValidationError('Incorrect mobile')


