from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'birth_date', 'vip_1', 'vip_2', 'vip_3', 'admin')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('author', 'text', 'image', 'topic')
