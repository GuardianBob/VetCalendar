from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .serializers import CalendarSerializer
from django.core import serializers
from .models import Calendar, Shift, ShiftType, Shift, ScheduleShift
from django.forms.models import model_to_dict
from .forms import QuickAddForm, ShiftTimeForm
from login.models import User, Address, CityState, Phone, AccessLevel, UserPrivileges, Occupation, User_Info
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .scripts import convert_schedule, get_users, load_schedule, set_form_fields, convert_to_shift_datetime, fix_timezone
import datetime, json, traceback, sys, re, pytz
from datetime import datetime, date, timedelta
import dateutil.parser as parser
# import numpy as np
from django.utils import timezone
from django.middleware.csrf import get_token
from dateutil.parser import parse
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
  options = Shift.objects.all()
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

month_abbrev = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

@csrf_exempt 
def upload_file(request):
  # print (request.POST['date'])
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

@csrf_exempt
def get_user_info(request):
  pass

@csrf_exempt
def get_shift_types(request):
  db_objects = ShiftType.objects.values()
  db_dict = [item for item in db_objects]
  db_json = json.dumps(db_dict)
  return HttpResponse(db_json)

@csrf_exempt
def get_shifts(request):
  db_objects = Shift.objects.values()
  db_dict = [item for item in db_objects]
  db_json = json.dumps(db_dict)
  return HttpResponse(db_json)

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def quick_add(request):
  try:
    if request.method == 'POST':
      content = json.loads(request.body)
      content = list(content[0].values())[0]
      print(content)
      user = User.objects.get(id=content['user'])
      shift = Shift.objects.get(id=content['shift'])
      shift_type = ShiftType.objects.get(id=content['shift_type'])
      # shift_date = datetime.strptime(content['shift_date'], "%Y-%m-%d").date()
      for date in content['shift_date']:
        shift_date = parse(date).date()
        shift_start = convert_to_shift_datetime(date, shift.start_time)
        shift_end = convert_to_shift_datetime(date, shift.end_time)
        print(f'start: {shift_start}, end: {shift_end}')
        existing_shift = ScheduleShift.objects.filter(user=user, shift_start__date=shift_start.date()).first()
        if existing_shift:
          print(existing_shift.shift_start)
          existing_shift.shift = shift
          existing_shift.shift_type = shift_type
          existing_shift.shift_start = shift_start
          existing_shift.shift_end = shift_end
          existing_shift.save()
          # return JsonResponse({'message':f'Shift(s) Updated'}, status=200)
        else:
          # If there's no existing shift, create a new one
          new_shift = ScheduleShift.objects.create(
            user=user, 
            shift_start=shift_start, 
            shift=shift, 
            shift_type=shift_type, 
            shift_end=shift_end
          )
      return JsonResponse({'message':f'Shift(s) Added/Updated'}, status=200)
    else:
      form = QuickAddForm()
      form = set_form_fields(form)
      print(form)
      options = get_shift_options()
      options = options + get_shift_type_options() + get_user_options()
      print(options)
      context = {
        'forms': {
          '': form,
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
def schedule_settings(request):
  try:
    if request.method == 'GET':
      shift_settings = Shift.objects.all().values('id', 'start_time', 'end_time', 'shift_label', 'shift_name')
      shift_dict = [shift for shift in shift_settings] # Convert QuerySet into List of Dictionaries
      # print(shift_dict)
      # shift_data = json.dumps(shift_dict) 
      shift_type = ShiftType.objects.all().values('id', 'shift_type', 'shift_color', 'type_label')
      type_dict = [shift for shift in shift_type]
      context = {
        'shift_settings': shift_dict,
        'type_settings': type_dict
      }
      return JsonResponse(context)
    else:
      print(request.body)
      content = json.loads(request.body)
      shift_settings = content['shift_settings']
      type_settings = content['type_settings']
      # content = list(content[0].values())[0]
      print(shift_settings)
      for item in shift_settings:
        shift = Shift.objects.get(id=item['id'])
        shift.start_time = item['start_time']
        shift.end_time = item['end_time']
        shift.shift_label = item['shift_label']
        shift.shift_name = item['shift_name']
        shift.save()
      for item in type_settings:
        shift_type = ShiftType.objects.get(id=item['id'])
        shift_type.shift_type = item['shift_type']
        shift_type.shift_color = item['shift_color']
        shift_type.type_label = item['type_label']
        shift_type.save()
      return JsonResponse({'message': 'Settings Updated'}, status=200)
  except Exception as e:
    return trace_error(e, True)