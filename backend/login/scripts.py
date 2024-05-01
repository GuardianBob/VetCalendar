from .models import PasswordReset
from django.contrib.auth.hashers import make_password
import random, secrets, re, traceback, sys
from django.utils import timezone

FORM_FIELD_LABELS = {
    "first_name": "First Name",
    "middle_name": "Middle Name",
    "last_name": "Last Name",
    "initials": "Initials",
    "nickname": "Nickname",
    "email": "E-Mail",
    "phone_number": "Phone Number",
    "phone_type": "Phone Type",
    "street": "Address",
    "street2": "Address Line 2",
    "address": "Address",
    "address_line2": "Address Line 2",
    "apt_num": "Apt #",
    "city": "City",
    "state": "State",
    "zipcode": "Zip Code",
    "password": "Password",
    "verify_password": "Verify Password",
    "occupation": "Occupation",
    "old_password": "Old Password",
    "new_password": "New Password",
    "verify_password": "Verify Password",
    "remember_me": "Remember Me",
}

FORM_FIELD_TYPES = {
  "first_name": "input",
  "middle_name": "input",
  "last_name": "input",
  "nickname": "input",
  "email": "email",
  "phone_number": "tel",
  "phone_type": "select",
  "street": "input",
  "street2": "input",
  "address": "input",
  "address_line2": "input",
  "apt_num": "input",
  "city": "input",
  "state": "select",
  "zipcode": "input",
  "password": "password",
  "verify_password": "password",
  "occupation": "select",
  "old_password": "password",
  "new_password": "password",
  "remember_me": "checkbox",
}

REQUIRED_FIELDS = [
  "first_name",
  "last_name",
  "email",
  "phone_number",
  "password",
]

def set_form_fields(form):
  new_form = {}
  field_names = list(form.fields.keys())
  for field in field_names:
    new_form[field] = {
      'label': FORM_FIELD_LABELS[field],
      'type': FORM_FIELD_TYPES[field],
      'value': '',
      'required': field in REQUIRED_FIELDS,
    }    
  return new_form

def password_expires_at():
  return timezone.now() + timezone.timedelta(hours=24)

def generate_password(user):
  password = secrets.token_urlsafe(15)
  reset_link = secrets.token_urlsafe(50)
  reset_code = random.randint(100000, 999999)
  print(password)
  user.set_password(password)
  user.save()
  new_user_password, created = PasswordReset.objects.update_or_create(
      user=user,
      defaults={
        'temp_password': password,
        'reset_requested': True,
        'reset_code': reset_code,
        'reset_link': reset_link,
        'expires_at': password_expires_at(),
      }
  )  
  new_password = {
    "decrypted" : password,
    "encrypted" : user.password,
    "reset_code": reset_code,
    "reset_link": reset_link,
    'expires_at': password_expires_at(),
  }
  return new_password

def get_settings_columns(data):
  # print("getting Columns: \n", data)
  headers = []
  for key, value in data.items():
    if 'id' not in key:
      transformed_key = key.replace('_', ' ').title()
      type = "text"
      if 'time' in key:
        type = "time"
      if 'color' in key:
        type = "color"
      if 'description' in key:
        type = "textarea"
      if 'permissions' in key or 'users' in key:
        type = "multi-select"
      if 'id' in key or 'name' in key:
        type = "fixed"
      headers.append({
        "name": key,
        "label": transformed_key,
        "field": key,
        "sortable": True,
        "align": 'left',
        "type": type
      })
  print(headers)
  return headers