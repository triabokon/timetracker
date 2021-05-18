from django import forms
from django.db import models
from django.contrib.auth.models import User


class UserForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, max_length=50)
