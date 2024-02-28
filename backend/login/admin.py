from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, Permission, AccessLevel
from django.contrib.auth.forms import UserChangeForm
# from .forms import CustomUserChangeForm
from .models import User
from django import forms


class CustomUserChangeForm(UserChangeForm):
    initials = forms.CharField(required=False)

    class Meta(UserChangeForm.Meta):
        model = User  # or your custom user model
        fields = '__all__'

class UserAdmin(DefaultUserAdmin):
    form = CustomUserChangeForm
    fieldsets = DefaultUserAdmin.fieldsets + (
        (None, {'fields': ('initials',)}),
    )

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'permission', 'description']

class AccessLevelAdmin(admin.ModelAdmin):
    list_display = ['access']
    filter_horizontal = ['permissions', 'users']

# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(AccessLevel, AccessLevelAdmin)