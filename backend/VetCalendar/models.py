from django.db import models
from login.models import User

class ShiftName(models.Model):
  shift_name = models.CharField(max_length = 50)
  shift_label = models.CharField(max_length = 50)
  start_time = models.TimeField()
  end_time = models.TimeField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class ShiftType(models.Model):
  shift_type = models.CharField(max_length=50)
  shift_color = models.CharField(max_length=50)
  type_label = models.CharField(max_length=50)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class UserInitials(models.Model):
  initials = models.CharField(max_length=4)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Shifts(models.Model):
  shift_name = models.ForeignKey(ShiftName, related_name= 'assignments', on_delete=models.CASCADE)

  shift_type = models.ForeignKey(ShiftType, related_name='assigned_types', on_delete=models.CASCADE)
  shift_start = models.DateTimeField(blank=True, null=True)
  shift_end = models.DateTimeField(blank=True, null=True)
  user = models.ForeignKey(User, related_name='user_shifts', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
class Calendar(models.Model):
  user_initials = models.CharField(max_length=10)
  shift = models.CharField(max_length=20)
  start = models.DateTimeField()
  end = models.DateTimeField()
  month = models.CharField(max_length=20)
  year = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Vacation(models.Model):
  user = models.ForeignKey(User, related_name='user_vacations', on_delete=models.CASCADE)
  start = models.DateTimeField()
  end = models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)