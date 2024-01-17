from django.db import models
from django.core import serializers
import json
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True)
    initials = models.CharField(max_length=10, blank=True)
    nickname = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Email(models.Model):
  email = models.EmailField(max_length=100)
  user = models.ForeignKey(User, related_name='user_email', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class PasswordReset(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    temp_password = models.CharField(max_length=128)
    reset_code = models.CharField(max_length=128)
    reset_link = models.CharField(max_length=128)
    reset_requested = models.BooleanField(default=False)
    reset_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=24))

class Address(models.Model):
  number = models.IntegerField(blank=True)
  street= models.CharField(max_length=100)
  street2 = models.CharField(max_length=100, blank=True)
  apt_num = models.CharField(max_length=15, blank=True)
  user = models.OneToOneField(User, related_name='user_address', on_delete=models.CASCADE, blank=True)  
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
  user = models.OneToOneField(User, related_name='user_city_state', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Phone(models.Model):
  phone_number = models.IntegerField()
  phone_type = models.CharField(max_length=50, default="mobile")
  users = models.ManyToManyField(User, related_name='user_phone')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class AccessLevel(models.Model):
  name = models.CharField(max_length=50)
  users = models.ManyToManyField(User, related_name='user_level', default=1)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

# class UserLevel(models.Model):
#   level = models.OneToOneField(AccessLevel, related_name='access_level', default=1, on_delete=models.CASCADE)
#   user = models.OneToOneField(User, related_name='user_level', on_delete=models.CASCADE)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

class UserPrivileges(models.Model):
  name = models.CharField(max_length=150)
  user = models.ManyToManyField(User, related_name="user_privileges", blank=True, default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Occupation(models.Model):
  occupation = models.CharField(max_length=50, default=0)
  user = models.ForeignKey(User, related_name='user_occupation', on_delete=models.CASCADE, default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class User_Info(models.Model):
  user = models.ForeignKey(User, related_name='user_info', on_delete=models.CASCADE)
  phone = models.ForeignKey(Phone, related_name='user_phone', on_delete=models.CASCADE)
  address = models.ForeignKey(Address, related_name='user_address', on_delete=models.CASCADE)
  city_state = models.ForeignKey(CityState, related_name='user_city_state', on_delete=models.CASCADE)
  level = models.ForeignKey(AccessLevel, related_name='user_level', on_delete=models.CASCADE)
  occupation = models.ForeignKey(Occupation, related_name='user_occupation', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
class FormOptions(models.Model):
  option_model = models.CharField(max_length=50, blank=True)
  option_field = models.CharField(max_length=50)
  option = models.CharField(max_length=50)
  option_label= models.CharField(max_length=50, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)