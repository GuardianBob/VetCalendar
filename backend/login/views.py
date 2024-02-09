from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from .models import User, Address, CityState, Phone, AccessLevel, UserPrivileges, Occupation, User_Info, Email, FormOptions, PasswordReset, AccountRequest
from django.db.models import Prefetch, Q
from django.contrib import messages
from django.contrib.auth import logout
import bcrypt, json
from django.middleware import csrf
from .forms import AccountRequestForm, Login_Form, UserAdminUpdateForm, UpdatePasswordForm, UpdateOccupationForm, UserInfoForm, AddressForm, CityStateForm, PhoneForm, EmailForm
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.forms.models import model_to_dict
import random, secrets, re, traceback, sys
from itertools import count
from django.contrib.auth import authenticate, login
from django.conf import settings
from datetime import timedelta
from django.core import serializers
from django.contrib.auth.hashers import make_password
from .scripts import set_form_fields, generate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
import logging.handlers

# class TokenVerifyView(APIView):
#   def post(self, request):
#     print("hit token verify")
#     token = request.data.get('token')
#     print(token)
#     if token is None:
#       print("token is None")
#       return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
#       # return JsonResponse({'message': 'Token is required'}, status=500)
#     try:
#       print("refresh token")
#       RefreshToken(token).check_blacklist()
#     except Exception as e:
#       print("exception")
#       return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

#     return Response({'status': 'Token is valid'}, status=status.HTTP_200_OK)

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
  
@csrf_exempt
def validate_token(request):
  # print(request.body)
  token = request.body.decode('utf-8')
  print(token)
  if token is None:
    print("token is None")
    return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
    # return JsonResponse({'message': 'Token is required'}, status=500)
  token_backend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
  try:
      print("validate access token")
      validated_token = token_backend.decode(token, verify=True)
      print(validated_token)
  except TokenError as e:
      print("exception")
      return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
  return Response({'status': 'Token is valid'}, status=status.HTTP_200_OK)

class SingleUser():
  pass

class UserProfile():
  pass

def trace_error(e, isForm=False):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    filename, line_number, func_name, text = traceback.extract_tb(exc_traceback)[0]
    error_message = f"An error occurred in file {filename} on line {line_number} in {func_name}(): {text}"
    logger.error(error_message)
    logger.error("Error: ", e)
    print(f"An error occurred in file {filename} on line {line_number} in {func_name}(): {text}")
    print("Error: ", e)
    if isForm:
        return JsonResponse({'message':'Form is invalid'}, status=500)
    return JsonResponse({'message':'Something went wrong'}, status=500)

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

def response_msg(status=200, message=""):
  response_data = {
    'code': status, # Replace this with your desired response code
    'message': message # Replace this with your desired response message
  }
  return JsonResponse(response_data, status=status)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print(response.data)  # This will print the response data to the console
        return response

# Create your views here.
@csrf_exempt
def user_login(request):
  try:
    if request.method == 'POST':
      req = request.POST
      print(req['email'])
      form = Login_Form(req)
      remember_me = req['remember_me']
      print(remember_me)
      if form.is_valid():
        # print("it worked!")
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        # user = validate_login(email, password)
        print(email)
        user = authenticate(request, username=req['email'], password=req['password'])
        print(user)
        if user is not None:        
          login(request, user)
          # Generate JWT token:
          # refresh = TokenObtainPairSerializer.get_token(user)
          if remember_me:
            # Set refresh token lifetime to 30 days if "Remember Me" is checked
            RefreshToken.lifetime = timedelta(days=15)
          else:
            # Otherwise, set it to 1 day
            RefreshToken.lifetime = timedelta(days=1)

          # Generate JWT token:
          refresh = RefreshToken.for_user(user)
          refresh['user_id'] = user.id
          refresh['admin'] = user.is_superuser
          return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
          }, status=200)
        else:
          # return response_msg(400, 'Incorrect Login or Password')
          return JsonResponse({"message":'Incorrect Login or Password'}, status=400)
      else:
        print("failed")
        print(form.errors)
        return JsonResponse({'message':'Incorrect Login or Password'}, status=400)
    else:
      form = Login_Form()
      context = {
        'form': form,
        'page_title': 'User Login:'   
      }
      return render(request, 'form.html', context)
    # return JsonResponse({'form': login_form.as_table()})
  except Exception as e:
    return trace_error(e, True)

@csrf_exempt
def login2(request, login_form = Login_Form()):
  if request.method == 'POST':
    print(request.POST)
    form = Login_Form(request.POST)
    if form.is_valid():
      print("it worked!")
      # email = form.cleaned_data['email']
      # password = form.cleaned_data['password']
      # print(email, password )
      # user = validate_login(email, password)
      user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
      # print('auth worked')
      # print(user)
      login(request, user)
      # if user is not None:
      #   # login(request, user)
      #   return HttpResponseRedirect('/users/')
      # else:
      #   # Show an error message
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
      # print(email.lower())
      user = User.objects.get(email=email.lower())
      # print(user)
    except User.DoesNotExist:
      return None
    # Check if the password is correct
    # print(user.password)
    # print(bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())
    # print(bcrypt.checkpw(password.encode(), user.password.encode()))
    if bcrypt.checkpw(password.encode(), user.password.encode()):
        return user
    return None

@csrf_exempt 
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_user(request):
  if request.method == 'POST':
    try:
      # data = request.POST.copy()
      data = json.loads(request.body.decode("utf-8"))
      # data = data[0]['Basic Info']
      data = list(data[0].values())[0]
      print(data)
      if not User.objects.filter(email__icontains=data['email']):
        phone_number = data['phone_number']
        if isinstance(phone_number, str):
          phone_number = re.sub('\D', '', phone_number)
        user, created = User.objects.update_or_create(
          username=data['email'],
          initials = get_unique_initials(data['first_name'], data['middle_name'], data['last_name']),
          defaults={
            'first_name': data['first_name'],
            'middle_name': data['middle_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'phone_number': phone_number,
            'phone_type': data['phone_type'],
            'nickname': data['nickname'],
          }
        )
        if created:
          generate_password(user)
  #   # print(request.POST)
  #   form = UserCreationForm(request.POST)
  #   if form.is_valid():
  #     # print('valid')
  #     # print(form.cleaned_data)
  #     if not verify_new_user(form.cleaned_data["email"]):
  #       # print('verified new')
  #       new_user = save_new_user(form.cleaned_data)
  #       return JsonResponse({'message':'New User Being Added'}, status=200)
  #     else:
  #       print('user exists')
  #       return JsonResponse({'message':'E-Mail already exists'}, status=500)
  #   print('guess not valid')
  #   return JsonResponse({'message':'Something went wrong'}, status=500)
  # else:
    # post_data['initials'] = get_unique_initials(post_data['first_name'], post_data['middle_name'], post_data['last_name'])
    # post_data['username'] = post_data['email']
    # user_form = UserInfoForm(post_data)
    # phone_form = PhoneForm(post_data)
    # # email_form = EmailForm(request.POST)
    # # address_form = AddressForm(request.POST)
    # # city_state_form = CityStateForm(request.POST)
    # print(user_form.is_valid(), phone_form.is_valid())
    # print(post_data['initials'], phone_form['phone_number'])
    # if user_form.is_valid() and phone_form.is_valid(): #and address_form.is_valid() and city_state_form.is_valid() 
    #   if not User.objects.filter(email__icontains=user_form.cleaned_data["email"]):
    #     user = user_form.save()
    #     user.initials = post_data['initials']  # Set initials
    #     user.username = post_data['email']  # Set username
    #     user.save()  # Now save to DB
    #     print("user: ", user.initials)
    #     phone = phone_form.save()
    #     phone.users.add(user)
    #     phone.save()
    #     # email = email_form.save(commit=False)
    #     # email.user = user
    #     # email.save()
    #     # address = address_form.save(commit=False)
    #     # address.user = user
    #     # address.save()
    #     # city_state = city_state_form.save(commit=False)
    #     # city_state.user = user
    #     # city_state.save()
    #     # login(request, user)
        return JsonResponse({'message':'New User Successfully Added'}, status=200)
      print("Email already exists")
      return JsonResponse({'message':'Email already exists'}, status=500)
    except Exception as e:
      return trace_error(e, True)
  else:
    user_form = UserInfoForm()
    form = set_form_fields(user_form)
    context = {
      'forms': {
        'Basic Info': form, 
      },
      'options': get_form_options(),
    }
    # return render(request, 'multiForm.html', context)
    return JsonResponse(context)
  print("something went wrong")
  return JsonResponse({'message':'Something went wrong'}, status=500)

def verify_new_user(email):
  print(email)
  user = User.objects.filter(email__icontains=email)
  return user

def get_unique_initials(first_name='', middle_name='', last_name=''):
  user_initials = first_name[0].capitalize() + last_name[0].capitalize()
  user_full_initials = f"{first_name[0].capitalize()}{middle_name[0].capitalize()}{last_name[0].capitalize()}" if middle_name else user_initials
  initial_dict = set(User.objects.filter(
    Q(initials__icontains=user_initials) | 
    Q(initials__icontains=user_full_initials)
  ).values_list("initials", flat=True))
  if user_initials in initial_dict:
    if middle_name:
      if user_full_initials not in initial_dict:
        return user_full_initials
    for counter in count(1):
      new_initials = f"{user_initials}{counter:02d}"
      if new_initials not in initial_dict:
        return new_initials
  return user_initials

def get_unique_username(first_name='', middle_name='', last_name=''):
  base_username = f"{first_name[0]}{middle_name[0] if middle_name else ''}{last_name}".lower()
  username_set = set(User.objects.filter(
    Q(username__icontains=base_username)
  ).values_list("username", flat=True))
  if base_username in username_set:
    for counter in count(1):
      new_username = f"{base_username}{counter:02d}"
      if new_username not in username_set:
        return new_username
  return base_username

def get_unique_initials_old(user_first_name='', user_middle_name='', user_last_name=''):
    print(f'First: {user_first_name}, Middle: {user_middle_name}, Last: {user_last_name}')
    user_initials = user_first_name[0] + user_last_name[0] 
    initial_dict = User.objects.filter(initials__icontains=user_initials).values("initials")
    # get the user's initials from just first and last name
    print(initial_dict)
    # user_initials = generate_new_initials(user_first_name, user_middle_name, user_last_name)
    if any(d["initials"] == user_initials for d in initial_dict):
      print("found first initials")
      if not user_middle_name == "":
        user_full_initials = user_first_name[0] + user_middle_name[0] + user_last_name[0]
        if not user_full_initials in initial_dict:
          return user_full_initials
      else:
        counter = 1
        new_initials = user_initials + f"{counter:02d}"
        while any(d["initials"] == new_initials for d in initial_dict):
            counter += 1
            new_initials = user_initials + f"{counter:02d}"
        user_initials = new_initials
        return user_initials
    return user_initials

# def save_new_user(user):
#   print(user["first_name"])
#   # Create a new user  
#   new_initials=get_unique_initials(user["first_name"], user["middle_name"], user["last_name"])
#   new_user = User.objects.create(
#       first_name=user["first_name"],
#       middle_name=user["middle_name"],
#       last_name=user["last_name"],
#       email=user["email"],
#       username=user["email"],
#       initials=new_initials.upper(),
#   )  
#   # Create a new user password
#   new_password=generate_password(new_user)
  
#   # Create a new phone for the new user
#   new_phone = Phone.objects.create(
#       number=re.sub('\D', '', user["phone"]),
#       type=user["phone_type"],
#   )
#   # Add the new phone to the new user's phones
#   new_phone.users.add(new_user)
#   # Save all of these objects to the database
#   # new_user.save()
#   # new_user_password.save()
#   # new_phone.save()
#   user_info = {
#     "user": new_user,
#     "user_password": new_password['decrypted'],
#     "user_phone": new_phone
#   }
#   return user_info

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
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
  print(request.body)
  user = User.objects.get(id=request.body)
  print(user.first_name + " " + user.last_name)
  user.delete()
  return JsonResponse({'message': 'User deleted'}, status=200)

@csrf_exempt
def register(request):
  print("registration function")
  return HttpResponse("Hit registration function")

@csrf_exempt
def account_request(request):
  try:
    if request.method == 'POST':
      data = json.loads(request.body.decode("utf-8"))
      data = list(data[0].values())[0]
      print(data)
      if not User.objects.filter(email__icontains=data['email']) and not AccountRequest.objects.filter(email__icontains=data['email']):
        phone_number = data['phone_number']
        if isinstance(phone_number, str):
          phone_number = re.sub('\D', '', phone_number)
        request, created = AccountRequest.objects.update_or_create(
          defaults={
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'phone_number': phone_number,
            'phone_type': data['phone_type'],
          }
        )
        print("hit account request POST")
        return JsonResponse({'message':'Request Sent'}, status=200)
      print("Request already made for that e-mail address.")
      return JsonResponse({'message':'Request already made for that e-mail address.'}, status=500)
      
    else:
      request_form = AccountRequestForm()
      form = set_form_fields(request_form)
      context = {
        'forms': {
          'User Info': form, 
        },
        'options': get_form_options(),
      }
      # return render(request, 'multiForm.html', context)
      return JsonResponse(context)
  except Exception as e:
    return trace_error(e, True)

# ================== NOTE: MOVED TO SCRIPTS.PY =======================
# def generate_password(user, password_length=20):
#   password = secrets.token_urlsafe(password_length)
#   reset_link = secrets.token_urlsafe(50)
#   reset_code = random.randint(100000, 999999)
#   # print(password)
#   hashed_pass = make_password(password)
#   # print(hashed_pass)
#   new_user_password, created = PasswordReset.objects.update_or_create(
#       user=user,
#       defaults={
#         'temp_password': hashed_pass,
#         'reset_requested': True,
#         'reset_code': reset_code,
#         'reset_link': reset_link,
#       }
#   )  
#   user.password = hashed_pass
#   user.save()
#   new_password = {
#     "decrypted" : password,
#     "encrypted" : hashed_pass,
#     "reset_code": reset_code,
#     "reset_link": reset_link,
#   }
#   return new_password

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
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_list(request):
    # print(request.META.get('HTTP_AUTHORIZATION'))
    # print(request.session)
    users = User.objects.select_related('user_level').values('id', 'first_name', 'last_name', 'initials', 'email', 'user_level__name')
    # print(users)
    user_dict = [user for user in users] # Convert QuerySet into List of Dictionaries
    user_data = json.dumps(user_dict)   
    # print(user_data)
    return HttpResponse(user_data)

# class UserListView(APIView):
#     # authentication_classes = [JWTAuthentication]
#     # permission_classes = [IsAuthenticated]

#     def get(self, request):
#         print(request.META.get('HTTP_AUTHORIZATION'))
#         print(request.session)
#         users = User.objects.select_related('user_level').values('id', 'first_name', 'last_name', 'initials', 'email', 'user_level__name')
#         print(users)
#         user_dict = [user for user in users] # Convert QuerySet into List of Dictionaries
#         user_data = json.dumps(user_dict)   
#         print(user_data)
#         return Response(user_data)

def form_to_dict(form):
  form.is_valid()
  print("cleaned data here:")
  print(name for name, field in form.fields.items())
  return {
    'fields': {name: str(field) for name, field in form.fields.items()},
    'data': form,
  }

# @csrf_exempt 
# @api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def get_user_profile_old(request):
#     if request.method == 'GET':
#       req = request.GET
#       print(req)
#       if req["admin"] == "true":
#         # profile = User.objects.filter(id=req["id"]).values(*fields_to_select)
#         user = User.objects.get(pk=req["id"])
#         address = Address.objects.get(user=user) if Address.objects.filter(user=user).count() > 0 else None
#         city_state = CityState.objects.get(user=user) if CityState.objects.filter(user=user).count() > 0 else None
#         phone = Phone.objects.get(users=user) if Phone.objects.filter(users=user).count() > 0 else None
#         # email = Email.objects.get(user=user) if Email.objects.filter(user=user).count() > 0 else None
#         occupation = Occupation.objects.get(user=user) if Occupation.objects.filter(user=user).count() > 0 else None
#         if user:
#           user_info_form = UserInfoForm(instance=user)
#           address_form = AddressForm(instance=address) if address else AddressForm()
#           # for field in address_form.fields.values():
#           #   field.required = True
#           city_state_form = CityStateForm(instance=city_state) if city_state else CityStateForm()
#           phone_form = PhoneForm(instance=phone) if phone else PhoneForm()
#           # email_form = EmailForm(instance=email) if email else EmailForm()
#           occupation_form = UpdateOccupationForm(instance=occupation) if occupation else UpdateOccupationForm()
#           context = {
#             'forms': {
#               'User Info': user_info_form,
#               'Address': address_form,
#               'CityState': city_state_form,
#               'Phone': phone_form,
#               # 'Additional Email': email_form,
#               'Occupation': occupation_form,
#             },
#             'page_title': 'Update User',
#             'id': 'update_user'
#           }
#           return render(request, 'multiForm.html', context)
#           # return JsonResponse(context, status=200)
#     # return JsonResponse(profile[0])
#     else:
#       return update_user(request)

@csrf_exempt
def update_user(request):
  try:
    data = request.POST
    print("data: ", data)
    # Create or update User
    user, created = User.objects.update_or_create(
      username=data['email'],
      defaults={
        'first_name': data['first_name'],
        'middle_name': data['middle_name'],
        'last_name': data['last_name'],
        'email': data['email'],
      }
    )
    if created:
      generate_password(user)
    if user.initials == '' and user.first_name != '' and user.last_name != '':
      initials = get_unique_initials(user.first_name, user.middle_name, user.last_name)
      user.initials = initials
      user.username = user.email
      user.save()

    # Create or update Address
    if data['street'].strip():
      address, created = Address.objects.update_or_create(
        user=user,
        defaults={
          'street': data['street'],
          'street2': data['street2'],
          'apt_num': data['apt_num'],
        }
      )

    # Create or update CityState
    if data['state'].strip():
      city_state, created = CityState.objects.update_or_create(
        user=user,
        defaults={
          'city': data['city'],
          'state': data['state'],
          'zipcode': data['zipcode'],
        }
      )

    # Create or update Phone
    if data['phone_number'].strip():
      phone_number = re.sub('\D', '', data['phone_number'])
      phone, created = Phone.objects.update_or_create(
        users=user,
        defaults={
          'phone_number': phone_number,
          'phone_type': data['phone_type'],
        }
      )
      
    # Create or update Occupation
    if data['occupation'].strip():
      occupation, created = Occupation.objects.update_or_create(
      user=user,
      defaults={
        'occupation': data['occupation'],
      }
      )

    return JsonResponse({'message': 'User updated'}, status=200)
  except Exception as e:
    return trace_error(e, True)

# @csrf_exempt 
# def get_user_profile2(request):
#     req = json.loads(request.body.decode("utf-8"))
#     # req = request.body
#     # print(req["id"], req["admin"])
#     print(req)
#     remove = ['created_at', 'updated_at', 'user_shifts', 'user_password']
#     fields = ProfileFields()    
#     fields_to_select = (
#       fields.user_fields 
#       + fields.address_fields 
#       + fields.citystate_fields 
#       + fields.phone_fields
#     )
#     fields_to_select = list(set(fields_to_select) - set(remove))
#     # fields.userpass_fields = list(set(fields.userpass_fields) - set(remove))
#     print(fields_to_select)
#     if req["admin"] == "true":
#       # profile = User.objects.filter(id=req["id"]).values(*fields_to_select)
#       user = User.objects.get(id=req["id"])
#       address = user.user_address if hasattr(user, 'user_address') else None
#       city_state = user.user_city_state if hasattr(user, 'user_city_state') else None
#       phone = user.user_phone.first() if hasattr(user, 'user_phone') else None
#       occupation = user.user_occupation if hasattr(user, 'user_occupation') else None
#     else:
#       profile = User.objects.filter(id=req["id"]).values(*fields_to_select)
#       print(profile[0])
    
#     data = {
#       'first_name': user.first_name,
#       'middle_name': user.middle_name,
#       'last_name': user.last_name,
#       'initials': user.initials,
#       'nickname': user.nickname,
#       'email': user.email,
#       'phone': phone.number if phone else '',
#       'phone_type': phone.type if phone else '',
#       'apt_num': address.apt_num if address else '',
#       'address': address.street if address else '',
#       'address_line2': address.street2 if address else '',
#       'city': city_state.city if city_state else '',
#       'state': city_state.state if city_state else '',
#       'zipcode': city_state.zipcode if city_state else '',
#       'occupation': occupation.name if occupation else '',
#     }
#     userDetails = UserAdminUpdateForm(data)
#     updatePassword = UpdatePasswordForm()
    
#     context = {
#       'forms': {
#         'Details': userDetails, 
#         'Update Password': updatePassword, 
#       },
#       'page_title': 'Update User'
#     }
#     return render(request, 'multiForm.html', context)
#     # return JsonResponse(profile[0])

def get_form_options():
  form_options = FormOptions.objects.filter(Q(option_model='phone') | Q(option_model='occupation'))
  options = [{'field': option.option_field, 'option': option.option, 'label': option.option_label} for option in form_options]
  return options

def get_user_address(user):
  address = user.user_address if hasattr(user, 'user_address') else None
  city_state = user.user_city_state if hasattr(user, 'user_city_state') else None
  data = {}
  if address:
    data['street'] = {'type': 'input', 'value': address.street}
    data['street2'] = {'type': 'input', 'value': address.street2}
    data['apt_num'] = {'type': 'input', 'value': address.apt_num}
  else:
    data['street'] = {'type': 'input', 'value': ''}
    data['street2'] = {'type': 'input', 'value': ''}
    data['apt_num'] = {'type': 'input', 'value': ''}
  if city_state:
    data['city'] = {'type': 'input', 'value': city_state.city}
    data['state'] = {'type': 'select', 'value': city_state.state}
    data['zipcode'] = {'type': 'input', 'value': city_state.zipcode}
  else:
    data['city'] = {'type': 'input', 'value': ''}
    data['state'] = {'type': 'select', 'value': ''}
    data['zipcode'] = {'type': 'input', 'value': ''}
  for key in data:
    if key in FORM_FIELD_LABELS:
      data[key]['label'] = FORM_FIELD_LABELS[key]
  return data

def get_user_phone(user):
  phone = user.user_phone.first() if hasattr(user, 'user_phone') else None
  data = {}
  if phone:
    # print(phone)
    data['phone_number'] = {'type': 'input', 'value': phone.phone_number}
    data['phone_type'] = {'type': 'select', 'value': phone.phone_type}
  else:
    data['phone_number'] = {'type': 'input', 'value': ''}
    data['phone_type'] = {'type': 'select', 'value': ''}
  for key in data:
    if key in FORM_FIELD_LABELS:
      data[key]['label'] = FORM_FIELD_LABELS[key]
  return data

def get_user_occupation(user):
  occupation = user.user_occupation.first() if hasattr(user, 'user_occupation') else None
  data = {}
  if occupation:
    # print("occupation: ", occupation.occupation)
    data['occupation'] = {'type': 'select', 'value': occupation.occupation}
  else:
    data['occupation'] = {'type': 'select', 'value': ''}
  for key in data:
    if key in FORM_FIELD_LABELS:
      data[key]['label'] = FORM_FIELD_LABELS[key]
  return data

def get_user_model_data(user_id, admin=False):
  pass

def get_user_data(request, user_id, admin=False):
  # print(user_id)
  # if req["admin"] == "true":
  # Fetch the user
  user = get_object_or_404(User, pk=user_id)
  data = {
    'first_name': { 'type': 'input', 'value': user.first_name},
    'middle_name': { 'type': 'input', 'value': user.middle_name},
    'last_name': { 'type': 'input', 'value': user.last_name},
    'email': { 'type': 'input', 'value': user.email},
    'phone_number': { 'type': 'tel', 'value': user.phone_number},
    'phone_type': { 'type': 'select', 'value': user.phone_type},
    'nickname': { 'type': 'input', 'value': user.nickname},
  }
  for key in data:
    if key in FORM_FIELD_LABELS:
      data[key]['label'] = FORM_FIELD_LABELS[key]
  
  options = get_form_options()
  context = {
    'forms': {
      'Basic Info': data,
      'Address': get_user_address(user),
      # 'Phone': get_user_phone(user),
      'Occupation': get_user_occupation(user),
    },
    'options': options,
  }
  # Return the data as JSON
  return JsonResponse(context)
    
@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request, id = 0):
  if request.method == 'GET':
    # print(id)
    user_data = get_user_data(request, id, True)
    # print(type(user_data), user_data)
    return user_data
  else:
    return update_user_profile(request)
  
def create_user_model(data):
  # Create or update User
  user, created = User.objects.update_or_create(
    username=data['email'],
    initials = get_unique_initials(data['first_name'], data['middle_name'], data['last_name']),
    defaults={
      'first_name': data['first_name'],
      'middle_name': data['middle_name'],
      'last_name': data['last_name'],
      'email': data['email'],
      'phone_number': data['phone_number'],
      'phone_type': data['phone_type'],
      'nickname': data['nickname'],
    }
  )
  if created:
    generate_password(user)
  return user

def update_user_model(user, data):
  # user = User.objects.get(email=data['email'])
  user_info_form = UserInfoForm(data, instance=user)
  if user_info_form.is_valid():
    print("valid")
    user_info_form.save()
  else:
    print("Basic invalid")
    print(user_info_form.errors)
  return

def update_address_city_model(user, data):
  try:
    try:
      # Try to get the existing address
      address = user.user_address
    except User.user_address.RelatedObjectDoesNotExist:
      # If the user doesn't have an address, create a new one
      if data['street'] == '':
        print("no address data")
        return JsonResponse({'error': 'No Address'}, status=500)
      address = Address.objects.create(user=user)
    address_form = AddressForm(data, instance=address)
    if address_form.is_valid():
      address_form.save()
    else:
      print("Address invalid")
      print(address_form.errors)
    try:
      # Try to get the existing address
      city_state = user.user_city_state
    except User.user_city_state.RelatedObjectDoesNotExist:
      # If the user doesn't have an city_state, create a new one
      if data['city'] == '' and data['state'] == '' and data['zipcode'] == '':
        print("no city_state data")
        return 
      city_state = CityState.objects.create(user=user)
    city_state_form = CityStateForm(data, instance=city_state)
    if city_state_form.is_valid():
      city_state_form.save()
    else:
      print("CityState invalid")
      print(city_state_form.errors)
    # city_state_form = CityStateForm(value, instance=user.user_city_state)
    # if city_state_form.is_valid():
    #   city_state_form.save()
    print("address and city_state updated")
    return
  except Exception as e:
    return trace_error(e, True)

def update_occupation_model(user, data):
  try:
    # Try to get the existing address
    occupation = user.user_occupation.first()
  except User.user_occupation.RelatedObjectDoesNotExist:
    # If the user doesn't have an occupation, create a new one
    return
  if occupation is None:
    # If the user doesn't have an occupation, skip to the next iteration
    if data['occupation'] == '':
      return
    occupation = Occupation.objects.create(user=user)
  occupation_form = UpdateOccupationForm(data, instance=occupation)
  if occupation_form.is_valid():
    occupation_form.save()
  # occupation = user.user_occupation.get()
  # occupation_form = UpdateOccupationForm(value, instance=occupation)
  # if occupation_form.is_valid():
  #   occupation_form.save() 
  return

@csrf_exempt
def update_user_profile(request):
  if request.method == 'POST':
    # resp = request.data  # or request.data if you're using Django REST Framework
    data = json.loads(request.body.decode("utf-8"))
    print(data)
    # print(resp['Basic Info'])
    for item in data:
      for key, value in item.items():
        # print(key)
        # # Get the user
        # user = User.objects.get(email=data['Basic Info']['email'])
        if key == 'Basic Info':
          user = User.objects.get(email=value['email'])
          result = update_user_model(user, value)
          if isinstance(result, str):  # If the result is an error message
            print("An error occurred:", result)
            return JsonResponse({'error': result}, status=500)
          # user_info_form = UserInfoForm(value, instance=user)
          # if user_info_form.is_valid():
          #   print("valid")
          #   user_info_form.save()
          # else:
          #   print("Basic invalid")
          #   print(user_info_form.errors)
        elif key == 'Address':
          result = update_address_city_model(user, value)
          if isinstance(result, str):  # If the result is an error message
            print("An error occurred:", result)
            return JsonResponse({'error': result}, status=500)
          # try:
          #   # Try to get the existing address
          #   address = user.user_address
          # except User.user_address.RelatedObjectDoesNotExist:
          #   # If the user doesn't have an address, create a new one
          #   if value['street'] == '' or value['street2'] == '' or value['apt_num'] == '':
          #     continue
          #   address = Address.objects.create(user=user)
          # address_form = AddressForm(value, instance=address)
          # if address_form.is_valid():
          #   address_form.save()

          # try:
          #   # Try to get the existing address
          #   city_state = user.user_city_state
          # except User.user_city_state.RelatedObjectDoesNotExist:
          #   # If the user doesn't have an city_state, create a new one
          #   if value['city'] == '' and value['state'] == '' and value['zipcode'] == '':
          #     continue
          #   city_state = CityState.objects.create(user=user)
          # city_state_form = CityStateForm(value, instance=city_state)
          # if city_state_form.is_valid():
          #   city_state_form.save()
          # # city_state_form = CityStateForm(value, instance=user.user_city_state)
          # # if city_state_form.is_valid():
          # #   city_state_form.save()

        elif key == 'Occupation':
          result = update_occupation_model(user, value)
          if isinstance(result, str):  # If the result is an error message
            print("An error occurred:", result)
            return JsonResponse({'error': result}, status=500)
          # try:
          #   # Try to get the existing address
          #   occupation = user.user_occupation.first()
          # except User.user_occupation.RelatedObjectDoesNotExist:
          #   # If the user doesn't have an occupation, create a new one
          #   continue
          # if occupation is None:
          #   # If the user doesn't have an occupation, skip to the next iteration
          #   if value['occupation'] == '':
          #     continue
          #   occupation = Occupation.objects.create(user=user)
          # occupation_form = UpdateOccupationForm(value, instance=occupation)
          # if occupation_form.is_valid():
          #   occupation_form.save()
          # # occupation = user.user_occupation.get()
          # # occupation_form = UpdateOccupationForm(value, instance=occupation)
          # # if occupation_form.is_valid():
          # #   occupation_form.save() 

    return JsonResponse({'message': 'User updated successfully'})

  else:
    return JsonResponse({'error': 'Invalid request method'}, status=400)

