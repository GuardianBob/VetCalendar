from django.contrib import admin
from .models import Shift

class ShiftAdmin(admin.ModelAdmin):
  list_display = ('shift_name', 'shift_label', 'start_time', 'end_time')

admin.site.register(Shift, ShiftAdmin)