from django.contrib import admin
from .models import ShiftName, FormBuilder

class ShiftAdmin(admin.ModelAdmin):
  list_display = ('shift_name', 'shift_label', 'start_time', 'end_time')

admin.site.register(FormBuilder)
admin.site.register(ShiftName, ShiftAdmin)