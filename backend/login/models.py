from django.db import models
from django.core import serializers
from django.conf import settings
import json
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  middle_name = models.CharField(max_length=50, blank=True)
  initials = models.CharField(max_length=10, blank=True)
  nickname = models.CharField(max_length=50, blank=True)
  phone_number = models.CharField(max_length=50, blank=True)
  phone_type = models.CharField(max_length=50, default="mobile")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def delete(self, *args, **kwargs):
    self.user_phone.all().delete()  # Delete all related phone numbers
    self.user_level.all().delete()  # Delete all related access levels
    self.user_privileges.all().delete()  # Delete all related privileges
    super().delete(*args, **kwargs)  # Call the original delete method

# class Email(models.Model):
#   email = models.EmailField(max_length=100)
#   # user = models.ForeignKey(User, related_name='user_email', on_delete=models.CASCADE)
#   user = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

class PasswordReset(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  temp_password = models.CharField(max_length=128)
  reset_code = models.CharField(max_length=128)
  reset_link = models.CharField(max_length=128)
  reset_requested = models.BooleanField(default=False)
  reset_used = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  expires_at = models.DateTimeField()

class Address(models.Model):
  number = models.IntegerField(blank=True, null=True)
  street= models.CharField(max_length=100)
  street2 = models.CharField(max_length=100, blank=True, null=True)
  apt_num = models.CharField(max_length=15, blank=True, null=True)
  # user = models.OneToOneField(User, related_name='user_address', on_delete=models.CASCADE, blank=True, null=True)  
  user = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  @property
  def street_address(self):
    return f"{self.number} {self.street} {self.street2} {self.apt} {CityState.city} {CityState.state} {CityState.zipcode}"
    # NOTE: Double check, the city, state and zip here may not work
  
class CityState(models.Model):
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=10)
  zipcode = models.IntegerField()
  # user = models.OneToOneField(User, related_name='user_city_state', on_delete=models.CASCADE)
  user = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Phone(models.Model):
  phone_number = models.IntegerField()
  phone_type = models.CharField(max_length=50, default="mobile")
  users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_phone')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Permission(models.Model):
  permission = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.permission

class AccessLevel(models.Model):
  access = models.CharField(max_length=255)
  permissions = models.ManyToManyField(Permission, related_name='access_levels', blank=True)
  users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='access_levels', blank=True)

  def __str__(self):
    return self.access  

class Occupation(models.Model):
  occupation = models.CharField(max_length=50, default=0)
  # user = models.ForeignKey(User, related_name='user_occupation', on_delete=models.CASCADE)
  user = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
class FormOptions(models.Model):
  option_model = models.CharField(max_length=50, blank=True, null=True)
  option_field = models.CharField(max_length=50)
  option = models.CharField(max_length=50)
  option_label= models.CharField(max_length=50, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class AccountRequest(models.Model):
  first_name = models.CharField(max_length=50, blank=False)
  last_name = models.CharField(max_length=10, blank=False)
  email = models.CharField(max_length=50, blank=False)
  phone_number = models.CharField(max_length=50, blank=False)
  phone_type = models.CharField(max_length=50, default="Mobile")
  request_type = models.CharField(max_length=150, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)