from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from .models import User, User_Info
from django.contrib import messages
from django.contrib.auth import logout
import bcrypt, json
from django.middleware import csrf
from .forms import Register_Form, Login_Form
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import random

user_info_fields = [
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

lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
symbols = "@#$&_-()=%*:/!?+."

# Create your views here.
def login(request, login_form = Login_Form()):
  print("made it to views")
  context = {
    'login_form': login_form,
    'page_title': 'Login Form'    
  }
  return render(request, 'login.html', context)

@csrf_exempt
def validate(request):
  print("made it to validate")
  if request.method != "POST":
    return redirect("login")
  # print(request.method)
  body = json.loads(request.body)
  # print(bcrypt.hashpw(body['password'].encode(), bcrypt.gensalt()).decode())
  # print(body['email'], User.objects.filter(email=body['email']))
  if not len(User.objects.filter(email=body['email'])) > 0:
    return HttpResponseBadRequest('Invalid Email')
  else:
    stored_data = User.objects.get(email=body['email'])
    if not bcrypt.checkpw(body['password'].encode(), stored_data.password.encode()):
      return HttpResponseBadRequest('Invalid Email or Password')
  return JsonResponse({ 'response' : "All good!"})

@ensure_csrf_cookie
def get_csrf(request):
  token = csrf.get_token(request)
  return JsonResponse({'token' : token})

@csrf_exempt
def register(request):
  print("works!")
  return (HttpResponse("Hi."))

@csrf_exempt
def add_user(request):
  # try:
  data = eval(request.body.decode("utf-8"))
  if User.objects.filter(email=data["user__email"].lower()).count() > 0:
    print("User already exists")
    return HttpResponse("User already exists")
  # print(json.dumps(data))
  # print(type(data))
  password = ''
  pw_reset = False
  if "user__password" in data: 
    password = data["user__password"] 
  else: 
    password = generate_password()
    pw_reset = True
  initials = set_initials(data)
  # print(initials)
  # print(f'Password: {password}')
  middle_name = None
  middle_name = data["user__middle_name"].lower().capitalize() if "user__middle_name" in data else None
  new_user = User(
    first_name=data["user__first_name"].lower().capitalize(),
    last_name=data["user__last_name"].lower().capitalize(),
    middle_name = middle_name,
    email=data["user__email"].lower(),
    password=password["encrypted"],
    initials=initials,
    pw_reset=pw_reset
  )
  print(f'new user: {new_user.first_name} {new_user.last_name}')
  new_user.save()
  print(new_user.id)
  User_Info.objects.create(user=new_user)

  return HttpResponse("done")
  # except Exception as e:
  #   print(e)
  #   return HttpResponse(e)

def generate_password():
  string = lower + upper + numbers + symbols
  password = "".join(random.sample(string, 20))
  salted_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
  # print(salted_pass)
  new_password = {
    "decrypted" : password,
    "encrypted" : salted_pass
  }
  return new_password

def set_initials(data):
  print(data)
  initials = ''
  if 'user__middle_name' in data: 
    if data['user__middle_name'] != '':
      initials = data['user__first_name'][0].upper() + data['user__middle_name'][0].upper() + data['user__last_name'][0].upper()
  else:
    initials = data['user__first_name'][0].upper() + data['user__last_name'][0].upper()
  # print(f'initials: {initials}')
  # print(User.objects.filter(initials=initials).count())
  if User.objects.filter(initials=initials).count() > 0:
    count = 1
    while User.objects.filter(initials=initials+str(count)).count() > 0:
      count += 1
    initials=initials+str(count)
  return initials