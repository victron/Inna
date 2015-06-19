__author__ = 'vic'

from django import forms
from django.core.exceptions import ValidationError
from models import Dreams

class NewDreamForm(forms.Form):
    class Meta:
        model = Dreams




