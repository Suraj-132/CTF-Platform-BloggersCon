from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'username', 'email', 'mobile_number', 'score', 'is_active', 'is_staff']
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'mobile_number', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'bio', 'score')}),  # ✅ New section
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'mobile_number', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('score',)  # ✅ Prevent manual editing of score

admin.site.register(User, UserAdmin)
