from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, CharField
from django.forms.utils import ErrorList
from .models import Player
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])

class UserForm(UserCreationForm):
    # username = CharField(max_length=30, required=True, help_text="make it cute")
    # password = CharField(max_length=30, required=True, help_text="make it hard to crack")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
