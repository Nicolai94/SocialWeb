from django import forms
from django.contrib.auth.forms import UserCreationForm
from base.models import *


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        # widgets = {
        #     'host': forms.HiddenInput(attrs={
        #     }),
        #     'topic': forms.Select(attrs={
        #         'class': 'form-control',
        #         'placeholder': 'Enter the topic',
        #         'label': 'Enter the topic',
        #     })
        # }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']


class CustomLoginForm(forms.Form):
    class Meta:
        model = User
        fields = ['email', 'password']
