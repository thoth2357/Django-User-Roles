#import modules
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# Register your models here.

class UserAdminConfig(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'last_login', 'type')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'user_permissions',
            
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email','is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(Principal, UserAdminConfig)
admin.site.register(Teacher, UserAdminConfig)
admin.site.register(Student,UserAdminConfig)
admin.site.register(TeacherDetails)
admin.site.register(StudentDetails)
