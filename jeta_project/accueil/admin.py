from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Field, Theme, Question, Answer, PlayerProgress

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['username', 'top_score']

admin.site.register(CustomUser) 
admin.site.register(Field) 
admin.site.register(Theme) 
admin.site.register(Question) 
admin.site.register(Answer) 
admin.site.register(PlayerProgress) 
