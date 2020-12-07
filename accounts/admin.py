from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['id','username', 'avatar', 'email', 'age', 'title', 'description']
    #prepopulated_fields = {'slug': ('username',)}
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)