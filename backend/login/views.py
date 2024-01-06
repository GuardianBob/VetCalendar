from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from .models import User, UserPass, Address, CityState, Phone, AccessLevel, UserPrivileges, Occupation, User_Info
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth import logout
import bcrypt, json
from django.middleware import csrf
from .forms import Register_Form, Login_Form
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import random

class SingleUser():
    pass

class UserProfile():
    pass

class ProfileFields():
    user_fields = [f.name for f in User._meta.get_fields()]
    # userpass_fields = ['user_password__' + f.name for f in UserPass._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
    userpass_fields = ['user_password__password']
    address_fields = ['user_address__' + f.name for f in Address._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
    citystate_fields = ['user_city_state__' + f.name for f in CityState._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
    phone_fields = ['user_phone__' + f.name for f in Phone._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
    level_fields = ['user_level__' + f.name for f in AccessLevel._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
    privileges_fields = ['user_privileges__' + f.name for f in UserPrivileges._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
    occupation_fields = ['user_occupation__' + f.name for f in Occupation._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]

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
@csrf_exempt
def login(request, login_form = Login_Form()):
  if request.method == 'POST':
    print(request.POST)
    form = Login_Form(request.POST)
    if form.is_valid():
      # print("it worked!")
      email = form.cleaned_data['login_email']
      password = form.cleaned_data['login_password']
      user = validate_login(email, password)
      if user is not None:
        # login(request, user)
        response_data = {
          'code': 200, # Replace this with your desired response code
          'message': 'Success logged in' # Replace this with your desired response message
        }
        return JsonResponse(response_data)
      else:
        # Show an error message
        pass
  else:
      login_form = Login_Form()
  context = {
    'login_form': login_form,
    'page_title': 'Login Form'   
  }
  return render(request, 'login.html', context)
  # return JsonResponse({'form': login_form.as_table()})

@csrf_exempt
def login2(request, login_form = Login_Form()):
  if request.method == 'POST':
    print(request.POST)
    form = Login_Form(request.POST)
    if form.is_valid():
      print("it worked!")
      email = form.cleaned_data['login_email']
      password = form.cleaned_data['login_password']
      user = validate_login(email, password)
      if user is not None:
        # login(request, user)
        return HttpResponseRedirect('/users/')
      else:
        # Show an error message
        pass
  else:
      login_form = Login_Form()
  context = {
    'login_form': login_form,
    'page_title': 'Login Form'   
  }
  return render(request, 'login_copy.html', context)
  # return JsonResponse({'form': login_form.as_table()})

def validate_login(email, password):
    # Check if the user exists
    try:
      user = User.objects.get(email=email)
      print(user)
    except User.DoesNotExist:
      return None
    # Check if the password is correct
    print(user.password)
    print(bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())
    if bcrypt.checkpw(password.encode(), user.password.encode()):
        return user
    return None

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

@csrf_exempt
def get_user_list(request):
    users = User.objects.select_related('user_level').values('id', 'first_name', 'last_name', 'initials', 'email', 'user_level__level__name')
    print(users)
    user_dict = [user for user in users] # Convert QuerySet into List of Dictionaries
    user_data = json.dumps(user_dict)   
    print(user_data)
    return HttpResponse(user_data)

@csrf_exempt 
def get_user_profile(request):
    user_id = eval(request.body.decode("utf-8"))
    print(user_id)
    remove = ['created_at', 'updated_at', 'user_shifts', 'user_password']
    fields = ProfileFields()    
    fields_to_select = (
      fields.user_fields 
      + fields.address_fields 
      + fields.citystate_fields 
      + fields.phone_fields
    )
    fields_to_select = list(set(fields_to_select) - set(remove))
    # fields.userpass_fields = list(set(fields.userpass_fields) - set(remove))
    print(fields_to_select)
    profile = User.objects.filter(id=user_id).values(*fields_to_select)
    # profile = User.objects.filter(id=user_id).select_related('user_address', 'user_city_state', 'user_phone', 'user_level', 'user_privileges', 'user_occupation').prefetch_related(
    #   Prefetch('address_set', queryset=Address.objects.select_related(*fields.address_fields)),
    #   Prefetch('phone_set', queryset=Phone.objects.select_related(*fields.phone_fields)),
    #   Prefetch('citystate_set', queryset=CityState.objects.select_related(*fields.citystate_fields)),
    #   Prefetch('accesslevel_set', queryset=AccessLevel.objects.select_related(*fields.level_fields)),
    #   Prefetch('userprivileges_set', queryset=UserPrivileges.objects.select_related(*fields.privileges_fields)),
    #   Prefetch('occupation_set', queryset=Occupation.objects.select_related(*fields.occupation_fields))
    #   # Add other prefetch related calls for related models like 'citystate_set', etc.
    # )
    print(profile[0])
    # users = User.objects.values(*user_info_fields)
    # users = User.objects.select_related('user_password', 'user_address', 'user_city_state').all()
    # data = []
    # Loop through the QuerySet
    # for user in users:
    #     # Get the data for this user as a dictionary
    #     user_data = {
    #         "email": user.email,
    #         "first_name": user.first_name,
    #         "middle_name": user.middle_name,
    #         "last_name": user.last_name,
    #         "password": user.user_password.password,
    #         "pw_reset_code": user.user_password.pw_reset_code,
    #         "pw_reset": user.user_password.pw_reset,
    #         "number": user.user_address.number,
    #         "street": user.user_address.street,
    #         "street2": user.user_address.street2,
    #         "apt_num": user.user_address.apt_num,
    #     }

    #     # Add this user's data to the list
    #     data.append(user_data)
    # print("Data: \n", data)
    # profile = User.objects.select_related('user_password', 'user_address').values(
    #     'email', 'first_name', 'middle_name', 'last_name',
    #     'user_password__password', 'user_password__pw_reset_code', 'user_password__pw_reset',
    #     'user_address__number', 'user_address__street', 'user_address__street2', 'user_address__apt_num'
    # )
    # print("Users 2: \n:", list(profile))
    
    # address = Address.objects.get(pk=1)
    # users.user_address_set(address)
    # users.save()
    # print(users.values('email', 'first_name', 'last_name', 'user_password__password', 'user_address__number'))
    # print(users.address)
    # print(address.user.first_name)
    # user_dict = [user for user in users] # Convert QuerySet into List of Dictionaries
    # print(user_dict)
    # print(user_data)
    return JsonResponse(profile[0])

# @csrf_exempt
# def add_new_user: