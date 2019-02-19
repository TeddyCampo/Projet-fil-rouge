from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, CharField
from django.forms.utils import ErrorList
from .models import CustomUser
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'top_score')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'top_score')