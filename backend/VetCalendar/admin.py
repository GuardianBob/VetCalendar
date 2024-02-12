from django.contrib import admin
from .models import ShiftName

class ShiftAdmin(admin.ModelAdmin):
  list_display = ('shift_name', 'shift_label', 'start_time', 'end_time')

admin.site.register(ShiftName, ShiftAdmin)