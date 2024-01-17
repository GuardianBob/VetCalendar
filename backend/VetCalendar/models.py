from django.db import models
from login.models import User

# Create your models here.
class Todo(models.Model):
  title = models.CharField(max_length=120)
  description = models.TextField()
  completed = models.BooleanField(default=False)

  def _str_(self):
      return self.title
  
class Shift(models.Model):
  shift = models.CharField(max_length = 20)
  start_time = models.TimeField()
  end_time = models.TimeField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class ShiftType(models.Model):
  name = models.CharField(max_length=20)
  color=models.CharField(max_length=20)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class UserInitials(models.Model):
  initials = models.CharField(max_length=4)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class ScheduleShift(models.Model):
  date = models.DateField()
  shift = models.ForeignKey(Shift, related_name= 'assignments', on_delete=models.CASCADE)
  shift_type = models.ForeignKey(ShiftType, related_name='assigned_types', on_delete=models.CASCADE)
  user = models.ForeignKey(User, related_name='user_shifts', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
class Calendar(models.Model):
  user_initials = models.CharField(max_length=4)
  shift = models.CharField(max_length=20)
  start = models.DateTimeField()
  end = models.DateTimeField()
  month = models.CharField(max_length=20)
  year = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

# class AccessLevel(models.Model):
#   level = models.CharField(max_length=50)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

# class Occupation(models.Model):
#   occupation = models.CharField(max_length=50)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

# class UserRelations(models.Model):
#   user = models.ForeignKey(User, related_name='user_relations', on_delete=models.CASCADE)
#   level = models.ForeignKey(AccessLevel, related_name='user_level', on_delete=models.CASCADE)
#   occupation = models.ForeignKey(Occupation, related_name='user_occupation', on_delete=models.CASCADE)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)