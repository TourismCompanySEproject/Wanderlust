from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.forms import UserCreationForm
from django import forms

class AdminUser(UserCreationForm):
    email = forms.CharField(max_length = 30, required = True, widget= forms.EmailInput())
    password1 = forms.CharField(widget= forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    is_admin = forms.BooleanField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_admin')


