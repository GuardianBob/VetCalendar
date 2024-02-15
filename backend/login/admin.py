from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, Permission, AccessLevel
from .forms import CustomUserChangeForm

class UserAdmin(DefaultUserAdmin):
    form = CustomUserChangeForm

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'permission', 'description']

class AccessLevelAdmin(admin.ModelAdmin):
    list_display = ['access']
    filter_horizontal = ['permissions', 'users']

# admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(AccessLevel, AccessLevelAdmin)