__author__ = 'vic'

from django import forms

class LoginForm(forms.Form):
    user_name = forms.CharField(label='login', max_length=50)
    user_password = forms.PasswordInput()
