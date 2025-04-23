from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    inn = forms.CharField(max_length=12, label='ИНН', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'inn', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться'))