from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import *


User = get_user_model()

class UserAdmin(BaseUserAdmin):
    
    list_display = ('email', 'id', 'name', 'surname', 'phone_number','is_active','role')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('name', 'surname', 'email','phone_number')}),
        ('Permissions', {'fields': ('is_active','role')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name','surname', 'password1', 'password2')}
        ),
    )
    readonly_fields = ('timestamp',)
    search_fields = ('email', 'name', 'surname',)
    ordering = ('email',)
    filter_horizontal = ()


    def has_permission(self, request):
        """Grant all admin access if the user has role='admin'."""
        return request.user.is_authenticated and request.user.role == 'admin'
   


admin.site.register(User, UserAdmin)
