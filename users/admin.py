from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form     = CustomUserCreationForm
    form         = CustomUserChangeForm
    model        = CustomUser
    list_display = ['email', 'username', 'is_headhunter', 'date_joined']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': (
            'first_name', 'last_name', 'email', 'phone', 'state', 'is_headhunter', 
        )}),
        (('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
                ),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)