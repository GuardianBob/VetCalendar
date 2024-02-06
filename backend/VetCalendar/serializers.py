from rest_framework import serializers
from .models import Calendar

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ('id', 'user_initials', 'shift', 'start', 'end', 'month', 'year')