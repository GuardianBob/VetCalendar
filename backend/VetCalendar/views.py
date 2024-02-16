from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.db.models import ForeignKey, ManyToManyField, Q
from django.http import JsonResponse
from .serializers import CalendarSerializer
from django.core import serializers
from .models import Calendar, ShiftName, ShiftType, ShiftName, Shifts, FormBuilder
from django.forms.models import model_to_dict
from .forms import QuickAddForm, ShiftNameForm
from login.models import User, Address, CityState, Phone, AccessLevel, Permission, Occupation
from login.forms import AccessLevelForm, PermissionForm
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .scripts import convert_schedule, get_users, load_schedule, set_form_fields, convert_to_shift_datetime, fix_timezone, convert_label
from login.scripts import get_settings_columns
from login.views import create_user_new
import datetime, json, traceback, sys, re, pytz, os
from datetime import datetime, date, timedelta
import dateutil.parser as parser
# import numpy as np
from django.utils import timezone
from django.middleware.csrf import get_token
from dateutil.parser import parse
from django.apps import apps
from importlib import import_module
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
import datetime
import logging.handlers

# Create your views here.
# Create a logger
logger = logging.getLogger(__name__)

# Set the log level
logger.setLevel(logging.ERROR)

# Create a rotating file handler
handler = logging.handlers.RotatingFileHandler('error.log', maxBytes=20000, backupCount=5)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

@ensure_csrf_cookie
def get_csrf(request):
  token = get_token(request)
  print('token: ', token)
  return JsonResponse({'token' : token})

month_list = {
  "Jan": "01",
  "Feb": "02",
  "Mar": "03",
  "Apr": "04",
  "May": "05",
  "Jun": "06",
  "Jul": "07",
  "Aug": "08",
  "Sep": "09",
  "Oct": "10",
  "Nov": "11",
  "Dec": "12"
}

user_info_fields = [
  "email",
  "first_name",
  "middle_name",
  "last_name",
  "initials",
  "user_address__number",
  "user_address__street",
  "user_address__street2",
  "user_address__apt_num",
  "user_city_state__city",
  "user_city_state__state",
  "user_city_state__city_zip__zipcode",
  "user_level__level_name",
  "user_type__type_name"
  "user_type"
  # "user_address__values"
]

user_info_fields2 = [
  "user__id",
  "user__email",
  "user__first_name",
  "user__middle_name",
  "user__last_name",
  "user__initials",
  "user__user_phone__number",
  "user__user_phone__type",
  "address__number",
  "address__street",
  "address__street2",
  "address__apt_num",
  "city_state__city",
  "city_state__state",
  "city_state__city_zip__zipcode",
  "level__level_name",
  "occupation__type_name"
  # "level__level_name",
  # "type__type_name"
  # "type"
  # "user_address__values"
]

FORM_OPTION_MODEL = {
  'AccessLevel': 'Permission'
}

FORM_OPTION_LABELS = {
  'Permission': 'permission',
}

JSON_FORM = {
  "form_name": "Add User", 
  "module": "login", 
  "table": "User", 
  "fields": {
    "first_name": { "label": "First Name", "type": "text", "value": None, "required": True, "model_edit_field": "first_name"},
    "last_name": {"label": "Last Name", "type": "text", "value": None, "required": True, "model_edit_field": "last_name"},
    "email": {"label": "E-Mail", "type": "text", "value": None, "required": True, "model_edit_field": "email"},
    "phone_number": {"label": "Phone Number", "type": "phone", "value": None, "required": False,"model_edit_field": "phone_number"},
    "phone_type": {"label": "Phone Type", "type": "select", "value": None, "required": False,"model_edit_field": "phone_type"}
  },
  "field_options": {
    "shift": {"field": "shift", "related_model": "ShiftName", "option_label": "shift_label", "option_value": "id", "type": "select"},
    "shift_type": {"field": "shift_type", "related_model": "ShiftType", "option_label": "type_label", "option_value": "id", "type": "select"},
    "user": {"field": "user", "related_model": "User", "option_label": "last_name", "option_value": "id", "type": "select"}
  },
  "custom_options": [
    {"field": "phone_type", "option": "Mobile", "label": "Mobile"},
    {"field": "phone_type", "option": "Home", "label": "Home"},
    {"field": "phone_type", "option": "Office", "label": "Office"},
    {"field": "phone_type", "option": "Other", "label": "Other"}
  ],
  "save_function": "add_user"
}

# ======== NOTE: Need to update this so Office Manager can set Hospital Timezone in Admin Settings =========
TIMEZONE = pytz.timezone('America/Los_Angeles')

def trace_error(e, isForm=False):
  exc_type, exc_value, exc_traceback = sys.exc_info()
  filename, line_number, func_name, text = traceback.extract_tb(exc_traceback)[0]
  print(f"An error occurred in file {filename} on line {line_number} in {func_name}(): {text}")
  print("Error: ", e)
  if isForm:
    return JsonResponse({'message':'Form is invalid'}, status=500)
  return JsonResponse({'message':'Something went wrong'}, status=500)


def get_shift_options():
  options = ShiftName.objects.all()
  options = [{'field': 'shift', 'option': option.id, 'label': option.shift_label} for option in options]
  return options

def get_shift_type_options():
  options = ShiftType.objects.all()
  options = [{'field': 'shift_type', 'option': option.id, 'label': option.type_label} for option in options]
  return options

def get_user_options():
  users = User.objects.all()
  users = [{'field': 'user', 'option': user.id, 'label': f'{user.last_name} ({user.initials})'} for user in users]
  return users

def get_form_options(field, app_name, model_name):
  pull_from = FORM_OPTION_MODEL[model_name] if model_name in FORM_OPTION_MODEL else model_name
  label = FORM_OPTION_LABELS[pull_from]
  model = apps.get_model(app_name, pull_from)
  options = model.objects.all()
  options = [{'field': field, 'option': option.id, 'label': getattr(option, label)} for option in options]
  return options

month_abbrev = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

@csrf_exempt 
def upload_file(request):
  print (request.POST['date'])
  input_date = request.POST["date"]
  # print(input_date[:3].isnumeric())
  if input_date[:3].isnumeric():
    input_date = datetime.strptime(input_date, '%Y %b') # Convert string date to datetime
  else: 
    input_date = datetime.strptime(input_date, '%b %Y')
  input_month = input_date.strftime('%m')  # Convert datetime to month number
  short_month = input_date.strftime('%b')  # Convert datetime to short month, ex: "Nov"
  year = input_date.strftime('%Y')  # convert datetime to YYYY
  # new_date = datetime.strptime(input_date, '%Y %b').strftime('%b')
  # print(input_date, input_date.strftime('%m'), input_date.strftime('%Y'))
  file_name = request.FILES['file']
  if short_month.lower() in file_name.name.lower():
    contents = load_schedule(file_name, input_month, year) # Run upload script
  else:
    file_month = "false"
    for month in month_abbrev:  # Verify that the file month matches the input month
      if month.lower() in file_name.name.lower():
        # print(month)
        file_month = month
    # print(file_name)
    # print(gmail)
    # contents = ''
    # print(user)
    # contents = convert_schedule(file_name, user, month, year)
    month = month_list[file_month[:3]] if file_month != "false" else input_month
    contents = load_schedule(file_name, month, year) # Run upload script
  # print("the contents are: ", contents) 
  return HttpResponse(contents)

@csrf_exempt 
def return_user_list(request):
  file_name = request.FILES['file']
  file_month = "false"
  for month in month_abbrev:
    if month.lower() in file_name.name.lower():
      # print(month)
      file_month = month
  users = get_users(file_name)
  # print("contents", users)
  content = json.dumps({"month": file_month, "users":users})
  return HttpResponse(content)

@csrf_exempt 
def return_shifts(request):
  # print(request.body)
  content = json.loads(request.body)
  # print(content["date"])
  start = content["date"]["start"]
  end = content["date"]["end"]
  events = []
  users = []
  shifts = Shifts.objects.values('id', 'shift_name__shift_name', 'shift_type__shift_color', 'shift_start', 'shift_end', 'user__id', 'user__initials','shift_name_id', 'shift_type_id').filter(shift_start__gte=start, shift_end__lte=end)
  if shifts:
    for shift in shifts:
      # print(shift)
      events.append({
        "id": shift['id'],
        "user_id": shift['user__id'],
        "user": shift['user__initials'],
        "start": str(shift['shift_start']),
        "end": str(shift['shift_end']),
        "color": shift['shift_type__shift_color'],
        "shift_name_id": shift['shift_name_id'],
        "shift_type_id": shift['shift_type_id'],
      })
      if not shift['user__initials'] in users: users.append(shift['user__initials'])
    results = {'shifts': events, 'users': users}
    # print(users, events)
    # print(timezone.now())
    return JsonResponse(results)
  else:
    return HttpResponse("No Shifts")
  
@csrf_exempt 
def return_shifts_old(request):
  # print(request.body)
  content = json.loads(request.body)
  # print(content["date"])
  start = content["date"]["start"]
  end = content["date"]["end"]
  shifts = Calendar.objects.filter(start__gte=start, end__lte=end)
  # print(shifts)
  events = []
  users = []
  if shifts:
    for shift in shifts:
      # print(shift.start)
      events.append({
        "id": shift.id,
        "user": shift.user_initials,
        "start": str(shift.start),
        "end": str(shift.end),
      })
      if not shift.user_initials in users: users.append(shift.user_initials)
    results = {'shifts': events, 'users': users}
    # print(users, events)
    # print(timezone.now())
    return JsonResponse(results)
  else:
    return HttpResponse("No Shifts")

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def quick_add(request):
  try:
    if request.method == 'POST':
      content = json.loads(request.body)
      # content = list(content[0].values())[0]
      # print(content)
      user = User.objects.get(id=content['user'])
      shift_name = ShiftName.objects.get(id=content['shift'])
      shift_type = ShiftType.objects.get(id=content['shift_type'])
      # shift_date = datetime.strptime(content['shift_date'], "%Y-%m-%d").date()
      for date in content['shift_date']:
        item = content
        item['shift_date'] = date
        # print(item)
        shift_date = parse(date).date()
        shift_start = convert_to_shift_datetime(date, shift_name.start_time)
        shift_end = convert_to_shift_datetime(date, shift_name.end_time)
        if shift_end < shift_start:
          shift_end = shift_end + datetime.timedelta(hours=24)
        print(f'start: {shift_start}, end: {shift_end}')
        existing_shift = Shifts.objects.filter(user=user, shift_start__date=shift_start.date()).first()
        if existing_shift:
          item['id'] = existing_shift.id
          print(item)
        shift = creat_update_shift(item)
        #   print(existing_shift.shift_start)
        #   existing_shift.shift = shift
        #   existing_shift.shift_type = shift_type
        #   existing_shift.shift_start = shift_start
        #   existing_shift.shift_end = shift_end
        #   existing_shift.save()
        #   # return JsonResponse({'message':f'Shift(s) Updated'}, status=200)
        # else:
        #   # If there's no existing shift, create a new one
        #   new_shift = Shifts.objects.create(
        #     user=user, 
        #     shift_start=shift_start, 
        #     shift=shift, 
        #     shift_type=shift_type, 
        #     shift_end=shift_end
        #   )
      return JsonResponse({'message':f'Shift(s) Added/Updated'}, status=200)
    else:
      form = QuickAddForm()
      form = set_form_fields(form)
      # print(form)
      options = get_shift_options()
      options = options + get_shift_type_options() + get_user_options()
      # print(options)
      context = {
        'forms': {
          '': form,
        },
        'options': options
      }
      print(context)
      return JsonResponse(context)
  except Exception as e:
    return trace_error(e, True)

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def schedule_settings(request):
  try:
    if request.method == 'GET':
      shift_settings = ShiftName.objects.all().values('id', 'start_time', 'end_time', 'shift_label', 'shift_name')
      shift_dict = [shift for shift in shift_settings] # Convert QuerySet into List of Dictionaries
      # print(shift_dict)
      # shift_data = json.dumps(shift_dict) 
      shift_type = ShiftType.objects.all().values('id', 'shift_type', 'shift_color', 'type_label')
      type_dict = [shift for shift in shift_type]
      # context = {
      #   'shift_settings': shift_dict,
      #   'type_settings': type_dict
      # }
      context = {
        'Edit Shift Settings': {
          'columns': get_settings_columns(shift_dict[0]),
          'data': shift_dict,
          'model': 'ShiftName'
        },
        'Edit Shift Type settings': {
          'columns': get_settings_columns(type_dict[0]),
          'data': type_dict,
          'model': 'ShiftType'
        },
    }
      return JsonResponse(context)
    else:
      # print(request.body)
      content = json.loads(request.body)
      # print(content)
      create_update_settings(content)
      # shift_settings = content['shift_settings']
      # type_settings = content['type_settings']
      # # print(shift_settings)
      # for item in shift_settings:
      #   shift = ShiftName.objects.get(id=item['id'])
      #   shift.start_time = item['start_time']
      #   shift.end_time = item['end_time']
      #   shift.shift_label = item['shift_label']
      #   shift.shift_name = item['shift_name']
      #   shift.save()
      # for item in type_settings:
      #   shift_type = ShiftType.objects.get(id=item['id'])
      #   shift_type.shift_type = item['shift_type']
      #   shift_type.shift_color = item['shift_color']
      #   shift_type.type_label = item['type_label']
      #   shift_type.save()
      return JsonResponse({'message': 'Settings Updated'}, status=200)
  except Exception as e:
    return trace_error(e, True)
  
def create_update_settings(settings):
  for setting in settings.values():
    print(setting)
    if 'data' in setting:
      if 'model' in setting:
        print(setting['model'])
        app_name = get_app_from_model(['VetCalendar', 'login'], setting['model'])
        Model = apps.get_model(app_name, setting['model'])  # Get the model dynamically          
        data = setting['data']
        print(data)
        for item in data:
          print(item['id'])
          item, created = Model.objects.update_or_create(
            id=item.get('id'),
            defaults={key: value for key, value in item.items() if key in [f.name for f in Model._meta.get_fields()]}
          )
  return 

def get_app_from_model(app_names, model_name):
  for app_name in app_names:
    try:
      apps.get_model(app_name, model_name)
      return app_name
    except LookupError:
      continue
  return None

def get_form(app_name, form_name):
  try:
    print(form_name)
    module = import_module(f'{app_name}.forms')
    form = getattr(module, form_name)
    return form()
  except (ImportError, AttributeError):
    return None
  
def find_key(nested_dict, target_values):
  print("Searching ====> :", nested_dict, target_values)
  for key, value in nested_dict.items():
    if isinstance(value, dict):
      if any(item in target_values for item in value.values()):
        return key
    elif value in target_values:
      return key
  return None

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_model_form(request, model=None):
  if request.method == 'GET':
    print(model)
    app_name = get_app_from_model(['VetCalendar', 'login'], model)
    form = get_form(app_name, f'{model}Form')
    # form = PermissionForm()
    form = set_form_fields(form, model)
    print(form)
    field = find_key(form, ['select', 'multi-select'])
    print(field)
    options = get_form_options(field, app_name, model)
    print(form, options)
    context = {
      'forms': {
        'Add New Item': form,
      },
      'model': model,
      'options': options,
    }
    return JsonResponse(context)
  else:
    content = json.loads(request.body)
    print(content)
    app_name = get_app_from_model(['VetCalendar', 'login'], content['model'])
    Model = apps.get_model(app_name, content['model'])
    item, created = Model.objects.update_or_create(
      id=content.get('id'),
      defaults={key: value for key, value in content.items() if key in [f.name for f in Model._meta.get_fields()]}
    )
    return JsonResponse({'message': 'Testing Backend'}, status=500)

  # Model = apps.get_model('VetCalendar', model)
  # print(Model)
  # form_items = Model.objects.values().first()
  # form_dict = [item for item in form_items]
  # print(form_dict)

  return JsonResponse({'message': 'Testing Backend'}, status=500)

@api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
@csrf_exempt
def get_keys(request):
  try:
    if request.method == 'POST':
      content = json.loads(request.body)
      keys = {}
      for item in content['data']:
        keys[item] = switch_api_key(item)

      # key = switch_api_key(content['data'])
      return JsonResponse(keys, status=200)
  except Exception as e:
    return trace_error(e, True)
  
def switch_api_key(value):
  try:
    return {
        'LOCAL_KEY': os.getenv('LOCAL_KEY'),
        'GOOGLE_CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID'),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
        'DISCOVERY_DOC': os.getenv('DISCOVERY_DOC'),
        'SCOPES': os.getenv('SCOPES'),
    }.get(value, 'No Key Found')
  except Exception as e:
    return trace_error(e, True)

# ============================ NOTE: MAy not be used ============================
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def save_schedule_updates(request):
  try:
    if request.method == 'POST':
      content = json.loads(request.body)
      for item in content:
        print(item)
        # shift = Shifts.objects.get(id=item['id'])
        # shift.shift_start = item['start']
        # shift.shift_end = item['end']
        # shift.save()
      return JsonResponse({'message': 'Shifts Updated'}, status=200)
  except Exception as e:
    return trace_error(e, True)
#================================================================================  

def creat_update_shift(data):
  shift_details = ShiftName.objects.get(id=data['shift'])
  if not data.get('user'):
    old_shift = Shifts.objects.get(id=data['id'])
    data['user'] = old_shift.user.id
  shift_start = convert_to_shift_datetime(data['shift_date'], shift_details.start_time)
  shift_end = convert_to_shift_datetime(data['shift_date'], shift_details.end_time)
  if shift_end < shift_start:
    shift_end = shift_end + datetime.timedelta(hours=24)
  # print(f'start: {shift_start}, end: {shift_end}')
  shift, created = Shifts.objects.update_or_create(
    id=data.get('id'),
    defaults={
      'shift_name_id': data['shift'],
      'shift_type_id': data['shift_type'],
      'shift_start': shift_start,
      'shift_end': shift_end,
      'user_id': data['user'],
    }
  )
  print('Created ===>: ', created)
  return shift
  
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def edit_event(request, id=None):
  try:
    if request.method == 'POST':
      content = json.loads(request.body)
      # content = list(content[0].values())[0]
      print(content)
      print(content['id'])
      creat_update_shift(content)

      return JsonResponse({'message': 'Shifts Updated'}, status=200)
    else:
      # shift = Shifts.objects.values('id', 'shift', 'shift_type', 'shift_start', 'shift_end', 'user').filter(id=id)
      event = get_object_or_404(Shifts, pk=id)
      print(event.shift_start.date())
      data = {
        'user': { 'type': 'select', 'value': event.user.id, 'label': 'User', 'required': True},
        'shift': { 'type': 'select', 'value': event.shift_name.id, 'label': 'Shift', 'required': True},
        'shift_type': { 'type': 'select', 'value': event.shift_type.id, 'label': 'Shift Type', 'required': True},
        'shift_date': { 'type': 'date', 'value': event.shift_start.date(), 'label': 'Shift Date', 'required': True},
        'id': { 'type': 'hidden', 'value': event.id},
      }
      print(data)
      options = get_shift_options()
      options = options + get_shift_type_options() + get_user_options()
      context = {
        'forms': {
          '': data,
        },
        'options': options
      }
      return JsonResponse(context)
  except Exception as e:
    return trace_error(e, True)
  
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def delete_event(request):
  try:
    if request.method == 'POST':
      content = json.loads(request.body)
      # print(content)
      shift = Shifts.objects.get(id=content['id'])
      # print(shift)
      shift.delete()
      return JsonResponse({'message': 'Shift Deleted'}, status=200)
  except Exception as e:
    return trace_error(e, True)
  
def add_edit_form(request, id=None):
  try:
    if request.method == 'POST':
      content = json.loads(request.body)
      print(content)
      # shift = Shifts.objects.get(id=content['id'])
      # print(shift)
      # shift.delete()
      return JsonResponse({'message': 'Testing Backend'}, status=500)
    else:

      return JsonResponse({'message': 'Testing Backend'}, status=500)
  except Exception as e:
    return trace_error(e, True)
    
  
def get_form_new(form_name):
  try:
    form = FormBuilder.objects.get(form_name=form_name)
    form_dict = {
      "fields": {},
      "options": [],
      "model": {form.module: form.table}
    }

    # Add fields to form_dict
    for field, options in form.fields.items():
      form_dict["fields"][field] = {
        "label": options.get('label', ''),
        "type": options.get('type', ''),
        "value": options.get('value', None),
        "required": options.get('required', False)
      }

    # Add field options to form_dict
    for option in form.field_options:
      form_dict["options"].append({
        "field": option.get('field', ''),
        "label": option.get('label', ''),
        "option": option.get('option', '')
      })

    return {"forms": {form.form_name: form_dict}}
  except FormBuilder.DoesNotExist:
      return {"error": f"Form with name {form_name} does not exist"}

def process_form_data(json_data):
  # Parse the JSON data
  data = json.loads(json_data)
  model_name = list(data['model'].values())[0]
  app_name = list(data['model'].keys())[0]

  # Get the model class
  ModelClass = apps.get_model(app_name, model_name)

  # Get the list of dates
  dates = data.pop('shift_date')

  # For each date, create or update a record
  for date in dates:
    data['shift_date'] = date
    obj, created = ModelClass.objects.update_or_create(defaults=data, shift_date=date, user=data['user'], shift=data['shift'], shift_type=data['shift_type'])

  return {"message": "Records created or updated successfully"}

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def form_builder(request):
  try:
    if request.method == 'GET':
      # get all fields from VetCalendar.FormBuilder model
      # fields = get_field_names(FormBuilder)
      # print(fields)
      fields = {
        "form_name": { "field": "form_name", "label": "Form Name", "type": "text", "required": True },
        "module":  { "field": "module", "label": "Module", "type": "select", "required": False },
        "table":  { "field": "table", "label": "Table", "type": "select", "required": True },
        "fields":  { "field": "fields", "label": "Fields", "type": "multi-select", "required": True },
        "field_options":  { "field": "field_options", "label": "Field Options", "type": "multi-select", "required": False },
        "custom_options":  { "field": "custom_options", "label": "Custom Options", "type": "multi-text", "required": False },
      }
      print("\n \n Updated fields: ====> ", fields)
      # build_form['fields'] = fields
      models_names = get_all_model_names_with_apps()
      print("Model Names: ====> ", models_names)
      table_options = []
      apps = []
      for model in models_names:
        table_options.append({
          "field": "table",
          "app": model['app'],
          "model": model['model'],
        })
        if not model['app'] in apps:
          apps.append(model['app'])
          table_options.append({
            "field": "module",
            "label": model['app'],
            "option": model['app'],
          })
      print("Table Options: ===> ", table_options)
      # build_form['options'] = table_options

      context = {
        "forms": {
          "Build Form": {
            "fields": fields,
            "options": table_options,
            "model": {"VetCalendar": "FormBuilder"}
          },
        },
      }
      return JsonResponse(context)
    else:
      return create_update_form(request)
  except Exception as e:
    return trace_error(e, True)

@csrf_exempt
def add_json_form(request):
  return JsonResponse({'message':'Testing...'}, status=200)
  
def get_field_names(app_name, model_name):
    model = apps.get_model(app_name, model_name)
    return [field.name for field in model._meta.get_fields()]

def get_all_model_names_with_apps():
    model_names = []
    django_apps = ['admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles']
    for model in apps.get_models():
      if model._meta.app_label not in django_apps:
        model_names.append({
            "model": model.__name__,
            "app": model._meta.app_label
        })
    return model_names

def get_app_name(model_name):
  model = apps.get_model('app_name', model_name)  # Replace 'app_name' with the name of your Django app
  return model._meta.app_label

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_table_fields(request):
  try:
    content = json.loads(request.body)
    print(content)
    field_names = get_field_names_and_related_fields(content['app'], content['model'])
    print(field_names)
    return JsonResponse({'fields': field_names})
  except Exception as e:
    return trace_error(e, True)
  
EXCLUDE_FIELDS = ["created_at", "updated_at"]
  
def get_field_names_and_related_fields(app_name, model_name):
  model = apps.get_model(app_name, model_name)
  fields = model._meta.get_fields()
  data = []
  for field in fields:
    if not field.name in EXCLUDE_FIELDS:
      if not field.auto_created and isinstance(field, (ForeignKey, ManyToManyField)):
        related_model = field.related_model
        # related_fields = ([f.name for f in related_model._meta.get_fields() if f.name == 'id' or not f.auto_created]) # Returns field names
        related_fields = [
          {"name": f.name, "type": f.get_internal_type()} 
          for f in related_model._meta.get_fields() 
          if f.name == 'id' or not f.auto_created
        ]
        data.append({
            "field": "fields",
            "label": field.name,
            "option": related_model.__name__,
            "app": app_name,
            "related_model": field.related_model.__name__,
            "related_fields": related_fields,
          })
      elif field.name == 'id' or not field.auto_created:
        data.append({
          "field": "fields",
          "label": field.name,
          "option": field.name,
          "app": app_name
          # "related_model": None,
          # "related_fields": None,
        })
  return data

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_field_options(request):
  try:
    print(request.body)
    content = json.loads(request.body)
    print(content)
    
    return JsonResponse({'message':'Testing...'}, status=200)
  except Exception as e:
    return trace_error(e, True)

def create_update_form(request):
  try:
    # print(request.body)
    content = json.loads(request.body)
    print(content)
    for form_name, form_data in content.items():
      fields = form_data.get('fields', {})
      options = form_data.get('field_options', None)
      custom = form_data.get('custom_options', None)
      model_data = form_data.get('table', None)
      module = list(model_data.keys())[0] if model_data else ''
      table = model_data.get(module, '')
      form_id = form_data.get('id') if form_data.get('id') else None
      field_options = {option['field']: option for option in options} if options else {}
      custom_options = {option['field']: option for option in custom if 'field' in option} if custom else {}
      save_function = form_data.get('save_function', None)
      print("Name: ", form_name, "\n Fields: ", fields, "\n Options", field_options, "\n Module: ", module, "Table: ", table)
      if form_id:
        try:
          form_builder = FormBuilder.objects.get(id=form_id)
          form_builder.form_name = form_name
          form_builder.module = module
          form_builder.table = table
          form_builder.fields = fields
          form_builder.field_options = field_options
          form_builder.custom_options = custom_options
          form_builder.save_function = save_function
          form_builder.save()
        except FormBuilder.DoesNotExist:
          form_builder = FormBuilder.objects.create(
              form_name=form_name,
              module=module,
              table=table,
              fields=fields,
              field_options=field_options,
              custom_options=custom_options,
              save_function=save_function,
            )
      else:
        form_builder = FormBuilder.objects.create(
          form_name=form_name,
          module=module,
          table=table,
          fields=fields,
          field_options=field_options,
          custom_options=custom_options,
          save_function=save_function,
        )

    return JsonResponse({'message':'Testing...'}, status=200)
  except Exception as e:
    return trace_error(e, True)
  
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_formbuilder_form(request, form=None, id=None):
  try:
    if request.method == 'POST':
      content = json.loads(request.body)
      # content = list(content[0].values())[0]
      for key in content:
        print(content[key])
        print(content[key]['function'])
        function = globals()[content[key]['function']]
        form_values = strip_form_content(content[key])
        function(form_values)
        # add_event(content[key])
      return JsonResponse({'message':f'Shift(s) Added/Updated'}, status=200)
    else:
      # content = json.loads(request.body)
      print(form)
      if form != None:
        form = FormBuilder.objects.values().get(form_name=form)
        # print(form['module'], form['table'], form['save_function'])
        if id:
          values = get_model_instance(form['module'], form['table'], id)
          # print(values)
          function = globals()[form['save_function']]
          form = function({'form': form, "values": values}, True)
        
          print("\n Saved Test: ====> \n", form)
        # Function to read form['field_options'] and pull model objects
        options = pull_model_options(form['field_options'])
        options.extend(form['custom_options'])
        print("Updated Options: ====> ", options)

        context = {
          'forms': {
            convert_label(form['form_name']): {
              "fields": form["fields"],
              'options': options,
              'model': { 'app': form['module'], 'model': form['table'] },
              'function': form['save_function']
            }
          },
        }
        # print(context)
        return JsonResponse(context)
      else:
        return JsonResponse({'message':'Request is invalid'}, status=500)
  except Exception as e:
    return trace_error(e, True)
  
def pull_model_options(field_options):
  options = []
  for item_key, item_value in field_options.items():
    related_model_name = item_value.get('related_model')
    option_label = item_value.get('option_label')
    if related_model_name and option_label:
      app_name, model_name = related_model_name.split('.')
      related_model = apps.get_model(app_name, model_name)
      model_objects = related_model.objects.all()
      for obj in model_objects:
        option = {
          'field': item_value['field'],
          'option': obj.id,
          'label': getattr(obj, option_label)
        }
        options.append(option)
  return options

def get_model_instance(app_name, model_name, id):
  Model = apps.get_model(app_name, model_name)
  instance = Model.objects.values().get(id=id)
  return instance

def strip_form_content(content):
  fields = {}
  for key, value in content['fields'].items():
    print(key, value)
    # fields[key] = value['value'] if isinstance(value['value'], list) else value['value']['value']
    if isinstance(value['value'], dict):
      fields[key] = value['value']['value']
    elif isinstance(value['value'], list):
      fields[key] = value['value']
    else:
      fields[key] = value['value']
    print(fields)
  return fields

def add_event(content, load=False):
  try:
    if load:
      print("\n====LOADING====\n", content['form'], "\n", content['values'])
      for key, item in content['form']['fields'].items():
        if item['type'] == 'date':
          item['value'] = content['values'][item['model_edit_field']].strftime('%b-%d-%Y')
        # if item['type'] == 'select':
        else:
          item['value'] = content['values'][item['model_edit_field']]
      # content['form']['fields']['user']['value'] = content['values']['user_id']
      # content['form']['fields']['shift']['value'] = content['values']['shift_name_id']
      # content['form']['fields']['shift_type']['value'] = content['values']['shift_type_id']
      # content['form']['fields']['shift_date']['value'] = content['values']['shift_start'].strftime('%b-%d-%Y')
      print("\n =====END LOADING====\n")
      return content['form']
    else:
    # content = {
    #   'fields': {
    #     'user': {'label': 'User', 'type': 'select', 'value': {'label': 'Meyer', 'value': 1}, 'required': True},
    #     'shift': {'label': 'Shift', 'type': 'select', 'value': {'label': 'Day', 'value': 1}, 'required': True},
    #     'shift_type': {'label': 'Shift Type', 'type': 'select', 'value': {'label': 'Switch', 'value': 6}, 'required': True},
    #     'shift_date': {'label': 'Shift Date', 'type': 'date', 'value': ['Feb-15-2024', 'Feb-16-2024'], 'required': True}},
    #   model': {
    #   'app': 'VetCalendar', 'model': 'Shifts'
    # }}
      fields = content
      # for key, value in content['fields'].items():
      #   fields[key] = value['value'] if isinstance(value['value'], list) else value['value']['value']
      # print(fields)
      user = User.objects.get(id=fields['user'])
      shift_name = ShiftName.objects.get(id=fields['shift'])
      shift_type = ShiftType.objects.get(id=fields['shift_type'])
      dates = [datetime.datetime.strptime(date, '%b-%d-%Y') for date in fields['shift_date']]
      # Get the earliest and latest dates
      earliest_date, latest_date = min(dates), max(dates)
      if earliest_date == latest_date:
        latest_date = earliest_date + datetime.timedelta(days=1)
      # print('date filter ====>: ', earliest_date, latest_date)
      # Filter the shifts
      existing_shifts = Shifts.objects.filter(
        Q(user=user),
        Q(shift_start__date__gte=earliest_date),
        Q(shift_start__date__lte=latest_date)
      ).values_list('shift_start__date', 'id')
      # print('Existing shifts===> :', existing_shifts)
      existing_shifts_dict = {date.strftime('%b-%d-%Y'): id for date, id in existing_shifts}
      for date in fields['shift_date']:
        item = fields.copy()
        item['shift_date'] = date
        # print(existing_shifts_dict)
        if date in existing_shifts_dict:
          item['id'] = existing_shifts_dict[date]
        # print(item)
        shift = creat_update_shift(item)
      return JsonResponse({'message':f'Shift(s) Added/Updated'}, status=200)
  except Exception as e:
    return trace_error(e, True)