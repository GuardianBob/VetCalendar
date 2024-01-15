from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import TodoSerializer, CalendarSerializer
from django.core import serializers
from .models import Todo, Calendar, Shift, ShiftType, Shift, ScheduleShift
from django.forms.models import model_to_dict
from login.models import User, UserPass, Address, CityState, Phone, AccessLevel, UserPrivileges, Occupation, User_Info
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .scripts import convert_schedule, test_calendar, test_event, get_users, load_schedule
import datetime, json
from datetime import datetime, date, timedelta
import dateutil.parser as parser
import numpy as np
from django.utils import timezone
from django.middleware.csrf import get_token

# Create your views here.

class SingleUser():
    pass

class UserProfile():
    pass

@ensure_csrf_cookie
def get_csrf(request):
    token = get_token(request)
    print('token: ', token)
    return JsonResponse({'token' : token})

class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

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
    year = input_date.strftime('%Y')    # convert datetime to YYYY
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
        print(users, events)
        # print(timezone.now())
        return JsonResponse(results)
    else:
        return HttpResponse("No Shifts")

@csrf_exempt 
def calendar_test(request):
    events = test_calendar()
    return HttpResponse(events) 

@csrf_exempt 
def event_test(request):
    new_event = test_event()
    return HttpResponse(new_event)



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


