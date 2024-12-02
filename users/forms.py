from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите ваш email'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите номер телефона'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Выберите страну'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control-file', 'accept': 'image/*'})

        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] += ' form-control'
