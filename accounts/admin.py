from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
# from .forms import RegisterForm
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    # add_form = RegisterForm
    list_display = ('phone', 'email', 'admin',)
    list_filter = ('staff', 'active', 'admin',)
    add_fieldsets = ('phone',)
    
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('phone', 'email', 'password',)}),
        ('Permissions', {'fields': (
            'admin','staff', 'active'
        )}),
    )
    search_fields = ('phone', 'email',)
    ordering = ('phone', 'email',)
    filter_horizontal=()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)