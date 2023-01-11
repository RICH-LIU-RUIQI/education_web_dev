import re

from django import forms
from apps.operations.models import UserFavorite


# class AddAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     mobile = forms.CharField(required=True, max_length=11)
#     course_name = forms.CharField(required=True, max_length=50)


class AddFavorForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        # fields = "__all__"
        # exclude = ['add_time']
        fields = ['fav_id', 'fav_type']



