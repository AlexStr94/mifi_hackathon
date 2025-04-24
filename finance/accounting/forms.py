from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    inn = forms.CharField(
        max_length=12,
        required=True,
        validators=[
            RegexValidator(
                regex='^[0-9]{10,12}$',
                message='ИНН должен содержать 10 или 12 цифр'
            )
        ],
        help_text='Введите ИНН (10 или 12 цифр)'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'inn', 'password1', 'password2')