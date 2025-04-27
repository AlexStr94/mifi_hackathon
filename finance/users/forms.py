from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User

class CustomUserCreationForm(UserCreationForm):
    inn = forms.CharField(
        max_length=12,
        validators=[RegexValidator(
            regex='^[0-9]{10,12}$',
            message='ИНН должен содержать 10 или 12 цифр'
        )],
        help_text='Введите ИНН (10 или 12 цифр)'
    )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'inn', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

    def clean_inn(self):
        inn = self.cleaned_data['inn']
        if User.objects.filter(inn__iexact=inn).exists():
            raise forms.ValidationError('Пользователь с таким ИНН уже существует.')
        return inn