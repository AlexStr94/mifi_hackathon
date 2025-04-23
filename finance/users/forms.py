from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    inn = forms.CharField(max_length=12, required=True, label='ИНН')

    class Meta:
        model = User
        fields = ('username', 'inn', 'password1', 'password2')