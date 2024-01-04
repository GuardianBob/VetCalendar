from django.db import models

# Create your models here.


class User(models.Model):
  email = models.CharField(max_length=100)
  password = models.CharField(max_length=50)
  first_name = models.CharField(max_length=50)
  middle_name = models.CharField(max_length=50, blank=True)
  last_name = models.CharField(max_length=50)
  initials = models.CharField(max_length=10, blank=True)
  nickname = models.CharField(max_length=50, blank=True)
  pw_reset = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  @property
  def full_name(self):
    return f"{self.first_name} {self.last_name}"

class Address(models.Model):
  number = models.IntegerField()
  street= models.CharField(max_length=100)
  street2 = models.CharField(max_length=100, blank=True)
  apt_num = models.CharField(max_length=15, blank=True)
  # user = models.ForeignKey(User, related_name='user_address', on_delete=models.CASCADE)  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  @property
  def street_address(self):
    return f"{self.number} {self.street} {self.street2} {self.apt} {CityState.city} {CityState.state} {CityState.zipcode}"
    # NOTE: Double check, the city, state and zip here may not work
  
class CityState(models.Model):
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=10)
  # user = models.ForeignKey(User, related_name='user_city_state', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  @property
  def zipcode(self):
    return f"{self.city_zip}"
  # NOTE: double check this actually works.

class Zipcode(models.Model):
  zipcode = models.IntegerField(max_length=15)
  city = models.ForeignKey(CityState, related_name='city_zip', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Phone(models.Model):
  number = models.IntegerField(max_length=15)
  type = models.IntegerField(max_length=15)
  users = models.ManyToManyField(User, related_name='user_phone')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class AccessLevel(models.Model):
  level_name = models.CharField(max_length=50, default=0)
  # user = models.ForeignKey(User, related_name='user_level', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Occupation(models.Model):
  type_name = models.CharField(max_length=50, default=0)
  # user = models.ForeignKey(User, related_name='user_occupation', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class User_Info(models.Model):
  user = models.ForeignKey(User, related_name='user_info', on_delete=models.CASCADE)
  # phone = models.ForeignKey(Phone, related_name='user_phone', on_delete=models.CASCADE)
  address = models.ForeignKey(Address, related_name='user_address', on_delete=models.CASCADE)
  city_state = models.ForeignKey(CityState, related_name='user_city_state', on_delete=models.CASCADE)
  level = models.ForeignKey(AccessLevel, related_name='user_level', on_delete=models.CASCADE)
  occupation = models.ForeignKey(Occupation, related_name='user_occupation', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
