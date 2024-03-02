from django.db import models
from login.models import User
from django_jsonform.models.fields import JSONField
from django.apps import apps

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

class FormBuilder(models.Model):
  # This model is used to store the form fields and options for building forms
  form_name = models.CharField(max_length=50)
  app = models.CharField(max_length=50) # The app/app the form is used for
  table = models.CharField(max_length=50) # The table/model the form is used for
  fields = models.JSONField() # The fields for the form ==> selected from table/model columns
  field_options = models.JSONField(blank=True, null=True) # The options for the fields ==> selected from table/model columns of models tied to the table/model by ForeignKey
  custom_options = models.JSONField(blank=True, null=True) # Custom options for the fields ex: phone types
  save_function = models.CharField(max_length=100, blank=True, null=True) # The function to call to save the form data
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class TableBuilder(models.Model):
  # This model is used to store the table fields and options for building tables
  table_name = models.CharField(max_length=50)
  app = models.CharField(max_length=50) # The app/app the table is used for
  table = models.CharField(max_length=50) # The table/model the table is used for
  columns = models.JSONField() # The columns (plus column) for the table ==> selected from table/model columns
  field_options = models.JSONField() # The options for the fields ==> selected from table/model columns of models tied to the table/model by ForeignKey
  custom_options = models.JSONField() # Custom options for the fields ex: phone types
  save_function = models.CharField(max_length=100, blank=True, null=True) # The function to call to save the form data
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class FormBuilderNew(models.Model):
  FULL_SCHEMA = {
    'type': 'dict', 
    'keys': {
      'form_name': {'type': 'string'},
      'app': {'type': 'string'},
      'model': {'type': 'string' },
      'fields': {
        'type' : 'array',
        'items': {
          'type': 'dict',
          'keys': {
            'field_name': {'type': 'string'},
            'settings': {
              'type': 'dict',
              'keys': {
                'label': {'type': 'string'},
                'type': {'type': 'string'},
                'value': {'type': 'string', 'default': ''},
                'required': {'type': 'boolean', 'default': False},
                'model_edit_field': {'type': 'string'},
              }
            },
          },
        },
      },
      'field_options': {
        'type': 'dict',
        'keys': {
          'option_name': {'type': 'string'},
          'settings': {
            'type': 'dict',
            'keys': {
              'field': {'type': 'string'},
              'related_model': {'type': 'string'},
              'option_label': {'type': 'string'},
              'option_value': {'type': 'string'},
              'type': {'type': 'string', 'default': 'select'},
            }
          }
        }
      },
      'custom_options': {
        'type': 'array',
        'items': {
          'type': 'dict',
          'keys': {
            'field': {'type': 'string'},
            'option': {'type': 'string'},
            'label': {'type': 'string'},
          }
        }
      }
    }
  }

  APP_CHOICES = {
    'type': 'string',
    'choices': ['VetCalendar', 'login']
  }

  FIELDS_SCHEMA = {
    'type' : 'array',
    'items': {
      'type': 'dict',
      'keys': {
        # 'field_name': {'type': 'string'},
        # 'settings': {
        'field_name': {'type': 'string'},
          # 'type': 'dict',
          # 'keys': {
          'label': {'type': 'string'},
          'type': {
            'type': 'string',
            'choices': ['text', 'select', 'date', 'phone', 'email', 'number', 'checkbox', 'time', 'textarea', 'multi-text', 'multi-select', 'multi-select-text', 'hidden', 'password', 'color'],
            },
          'value': {'type': 'string', 'default': ''},
          'required': {'type': 'boolean', 'default': False},
          'model_edit_field': {'type': 'string'},
          # }
        # }
      }
    }
  }

  FIELD_OPTIONS_SCHEMA = {
    'type': 'array',
    'items': {
      # 'option_name': {'type': 'string'},
      # 'settings': {
        'type': 'dict',
        'keys': {
          'field': {'type': 'string'},
          'related_model': {'type': 'string', 'title': 'Related Model (<app>.<model>) Ex: login.User'},
          'option_label': {'type': 'string', 'title': 'Model field that contains the field label'},
          'option_value': {'type': 'string'},
          'type': {
            'type': 'string',
            'choices': ['text', 'select', 'date', 'phone', 'email', 'number', 'checkbox', 'time', 'textarea', 'multi-text', 'multi-select', 'hidden', 'password', 'color'],
          },
        }
      # }
    }
  }

  CUSTOM_OPTIONS_SCHEMA = {
    'type': 'array',
    'items': {
      'type': 'dict',
      'keys': {
        'field': {'type': 'string'},
        'option': {'type': 'string'},
        'label': {'type': 'string'},
      }
    }
  }
  
  APP_CHOICES = [
    ('login', 'login'), 
    ('VetCalendar', 'VetCalendar')
  ]

  # def pre_save_hook(value):
  #   for item in value:
  #     if item['type'] == 'date':
  #       item['value'] = None if item['value'] == '' else item['value']  
  #   print(value)
  #   return value

  form_name = models.CharField(max_length=50)
  app = models.CharField(max_length=50, choices=APP_CHOICES) # The app/app the form is used for
  model = models.CharField(max_length=50) # The table/model the form is used for
  fields = JSONField(schema=FIELDS_SCHEMA, blank=True, null=True) # The fields for the form ==> selected from table/model columns
  field_options = JSONField(schema=FIELD_OPTIONS_SCHEMA, blank=True, null=True) # The options for the fields ==> selected from table/model columns of models tied to the table/model by ForeignKey
  custom_options = JSONField(schema=CUSTOM_OPTIONS_SCHEMA, blank=True, null=True) # Custom options for the fields ex: phone types
  save_function = models.CharField(max_length=100, blank=True, null=True) # The function to call to save the form data
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.form_name}  < {self.app} >  < {self.model} >"