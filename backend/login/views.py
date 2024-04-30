from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from .models import User, Address, CityState, Phone, AccessLevel, Permission, Occupation, FormOptions, PasswordReset, AccountRequest
from backend.utils import trace_error, process_forms_test, strip_form_content, send_text_email, send_html_email, save_model, delete_model, get_app_from_model
from django.db.models import Prefetch, Q
from django.contrib import messages
from django.contrib.auth import logout
import bcrypt, json
from django.middleware import csrf
from .forms import AccountRequestForm, Login_Form, UserAdminUpdateForm, UpdatePasswordForm, UpdateOccupationForm, UserInfoForm, AddressForm, CityStateForm, PhoneForm, PermissionForm, AccessLevelForm
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.forms.models import model_to_dict
import random, secrets, re, traceback, sys
from itertools import count
from django.contrib.auth import authenticate, login
from django.conf import settings
from datetime import timedelta
from django.core import serializers
from django.contrib.auth.hashers import make_password
from .scripts import set_form_fields, generate_password, get_settings_columns
from django.apps import apps
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

TEMP_ACCOUNT_REQUEST_FORM = {
  'Account Request': {
    'fields': [
      {'field_name': 'first_name', 'label': 'First Name', 'type': 'text', 'value': '', 'required': True, 'model_edit_field': 'first_name'},
      {'field_name': 'last_name', 'label': 'Last Name', 'type': 'text', 'value': '', 'required': True, 'model_edit_field': 'last_name'},
      {'field_name': 'email', 'label': 'E-Mail', 'type': 'email', 'value': '', 'required': True, 'model_edit_field': 'email'},
      {'field_name': 'phone_number', 'label': 'Phone Number', 'type': 'phone', 'value': '', 'required': False, 'model_edit_field': 'phone_number'},
      {'field_name': 'phone_type', 'label': 'Phone Type', 'type': 'select', 'value': '', 'required': False, 'model_edit_field': 'phone_type'}
    ], 
    'options': [
      {'field': 'phone_type', 'option': 'Mobile', 'label': 'Mobile'},
      {'field': 'phone_type', 'option': 'Home', 'label': 'Home'},
      {'field': 'phone_type', 'option': 'Office', 'label': 'Office'},
      {'field': 'phone_type', 'option': 'Other', 'label': 'Other'}
    ], 
    'model': {'app': 'login', 'model': 'AccountRequest'},
    'function': 'account_request', 
    'id': None
  }
}

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
    level_fields = ['access_levels__' + f.name for f in AccessLevel._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
    privileges_fields = ['user_privileges__' + f.name for f in Permission._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
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



# 

@csrf_exempt 
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
  print(request.body)
  content = json.loads(request.body)
  user = User.objects.get(id=content['id'])
  print(user.first_name + " " + user.last_name)
  user.delete()
  return JsonResponse({'message': 'User deleted'}, status=200)

@csrf_exempt
def register(request):
  print("registration function")
  return HttpResponse("Hit registration function")

@csrf_exempt
def request_access(request):
  print("request access function")
  try:
    content = json.loads(request.body)
    print(content)
    if not 'save' in content or not content['save']:
      content['forms'] = ['account_request']
      return process_forms_test(content)
    else:
      return account_request(content['forms'][0])
    # else:
    #   return JsonResponse({'message':'Request is invalid'}, status=500)
  except Exception as e:
    return trace_error(e, True)

@csrf_exempt
def account_request(content):
  try:
    form_values = strip_form_content(content)
    print(form_values['email'])
    if not User.objects.filter(email__icontains=form_values['email']) and not AccountRequest.objects.filter(email__icontains=form_values['email']):
      phone_number = form_values['phone_number']
      if isinstance(phone_number, str):
        phone_number = re.sub('\D', '', phone_number)
      request, created = AccountRequest.objects.update_or_create(
        defaults={
          'first_name': form_values['first_name'],
          'last_name': form_values['last_name'],
          'email': form_values['email'],
          'phone_number': phone_number,
          'phone_type': form_values['phone_type'],
        }
      )
      #   print("hit account request POST")
      return JsonResponse({'message':'Request Sent'}, status=200)
    print("Request already made for that e-mail address.")
    return JsonResponse({'message':'Request already made for that e-mail address.'}, status=500)
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
    users = User.objects.select_related('access_levels').values('id', 'first_name', 'last_name', 'initials', 'email', 'access_levels__access')
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
#         users = User.objects.select_related('access_levels').values('id', 'first_name', 'last_name', 'initials', 'email', 'access_levels__access')
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
  
def reset_user_password(data, id):
  try:
    print(data, id)
    if data['verify'] == True:
      user = User.objects.get(id=id)
      password = generate_password(user)
      message = f'''
        <p>Your password has been reset.</p>
        <p>Your temporary password is: <strong>{password['decrypted']}</strong></p>
      '''
      send_html_email("VSS Password Reset", message, [user.email])
      return JsonResponse({'message': 'User password has been reset'}, status=200)
    else:
      return JsonResponse({'message': 'Form was not validated'}, status=500)
  except Exception as e:
    return trace_error(e, True)
  pass

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

def get_access_options():
  permissions_obj = Permission.objects.all()
  users_obj = User.objects.values('id', 'last_name')
  permissions = [{'field': 'permissions', 'option': permission.id, 'label': permission.permission} for permission in permissions_obj]
  users = [{'field': 'users', 'option': user['id'], 'label': user['last_name']} for user in users_obj]
  return [permissions + users]

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
    initials = get_unique_initials(data['first_name'], None , data['last_name']),
    defaults={
      'first_name': data['first_name'],
      'middle_name': data['middle_name'] if 'middle_name' in data else '',
      'last_name': data['last_name'],
      'email': data['email'],
      'phone_number': data['phone_number'] if 'phone_number' in data else '',
      'phone_type': data['phone_type'] if 'phone_type' in data else '',
      # 'nickname': data['nickname'],
    }
  )
  if created:
    print("User created")
    user_password = generate_password(user)
    print(user_password)
    message = f'''
      <p>Thank you for registering with us. Your account has been created.</p>
      <p>Your temporary password is: <strong>{user_password['decrypted']}</strong></p>
    '''
    send_html_email("New User Account", message, [user.email])
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
  print("Updating Occupation")
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
    print(data['forms'])

    # print(resp['Basic Info'])
    user = None
    user_id = data['forms'][0]['id']
    user = User.objects.get(id=user_id)
    print(data['forms'][0]['id'])
    for item in data['forms']:
      # if item['model']['model'] == 'User':
      print(item['title'])
      if 'Basic Info' in item['title']:
        result = update_user_model(user, item)
        if isinstance(result, str):  # If the result is an error message
          print("An error occurred:", result)
          return JsonResponse({'error': result}, status=500)
      elif 'Address' in item['title']:
        result = update_address_city_model(user, item)
        if isinstance(result, str):  # If the result is an error message
          print("An error occurred:", result)
          return JsonResponse({'error': result}, status=500)
      elif 'Occupation' in item['title']:
          result = update_occupation_model(user, item)
          if isinstance(result, str):  # If the result is an error message
            print("An error occurred:", result)
            return JsonResponse({'error': result}, status=500)
      # for key, value in item.items():
      #   # print(key[0])
      #   # # Get the user
      #   # user = User.objects.get(email=data['Basic Info']['email'])
      #   # user = User.objects.get(email=value['email'])
      #   if key == 'Basic Info':
      #     result = update_user_model(user, value)
      #     if isinstance(result, str):  # If the result is an error message
      #       print("An error occurred:", result)
      #       return JsonResponse({'error': result}, status=500)
      #     # user_info_form = UserInfoForm(value, instance=user)
      #     # if user_info_form.is_valid():
      #     #   print("valid")
      #     #   user_info_form.save()
      #     # else:
      #     #   print("Basic invalid")
      #     #   print(user_info_form.errors)
      #   elif key == 'Address':
      #     result = update_address_city_model(user, value)
      #     if isinstance(result, str):  # If the result is an error message
      #       print("An error occurred:", result)
      #       return JsonResponse({'error': result}, status=500)
      #     # try:
      #     #   # Try to get the existing address
      #     #   address = user.user_address
      #     # except User.user_address.RelatedObjectDoesNotExist:
      #     #   # If the user doesn't have an address, create a new one
      #     #   if value['street'] == '' or value['street2'] == '' or value['apt_num'] == '':
      #     #     continue
      #     #   address = Address.objects.create(user=user)
      #     # address_form = AddressForm(value, instance=address)
      #     # if address_form.is_valid():
      #     #   address_form.save()

      #     # try:
      #     #   # Try to get the existing address
      #     #   city_state = user.user_city_state
      #     # except User.user_city_state.RelatedObjectDoesNotExist:
      #     #   # If the user doesn't have an city_state, create a new one
      #     #   if value['city'] == '' and value['state'] == '' and value['zipcode'] == '':
      #     #     continue
      #     #   city_state = CityState.objects.create(user=user)
      #     # city_state_form = CityStateForm(value, instance=city_state)
      #     # if city_state_form.is_valid():
      #     #   city_state_form.save()
      #     # # city_state_form = CityStateForm(value, instance=user.user_city_state)
      #     # # if city_state_form.is_valid():
      #     # #   city_state_form.save()

      #   elif key == 'Occupation':
      #     result = update_occupation_model(user, value)
      #     if isinstance(result, str):  # If the result is an error message
      #       print("An error occurred:", result)
      #       return JsonResponse({'error': result}, status=500)
      #     # try:
      #     #   # Try to get the existing address
      #     #   occupation = user.user_occupation.first()
      #     # except User.user_occupation.RelatedObjectDoesNotExist:
      #     #   # If the user doesn't have an occupation, create a new one
      #     #   continue
      #     # if occupation is None:
      #     #   # If the user doesn't have an occupation, skip to the next iteration
      #     #   if value['occupation'] == '':
      #     #     continue
      #     #   occupation = Occupation.objects.create(user=user)
      #     # occupation_form = UpdateOccupationForm(value, instance=occupation)
      #     # if occupation_form.is_valid():
      #     #   occupation_form.save()
      #     # # occupation = user.user_occupation.get()
      #     # # occupation_form = UpdateOccupationForm(value, instance=occupation)
      #     # # if occupation_form.is_valid():
      #     # #   occupation_form.save() 

    return JsonResponse({'message': 'User updated successfully'})

  else:
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def create_update_settings(settings):
  for setting in settings.values():
    if 'data' in setting:
      if 'model' in setting:
        # print(setting['model'])
        Model = apps.get_model('login', setting['model'])  # Get the model dynamically          
        data = setting['data']
        # print(data)
        for item in data:
          # print(item['id'])
          item, created = Model.objects.update_or_create(
            id=item.get('id'),
            defaults={key: value for key, value in item.items() if key in [f.name for f in Model._meta.get_fields()]}
          )
  return 

@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def master_settings(request):
  try:
    if request.method == 'POST':
      settings = json.loads(request.body)
      create_update_settings(settings)
      return JsonResponse({'message': 'Settings Updated!'}, status=200)
    elif request.method == 'DELETE':
      content = json.loads(request.body)
      model = content['model']
      id = content['id']
      print("Deleting ==========> : \n", f'Model : {model} \n', id)
      delete_model(model, id)
      return JsonResponse({'message': 'Setting Deleted'}, status=200)
    else:
      permissions = Permission.objects.all().values('id', 'permission', 'description')
      permission_dict = [permission for permission in permissions] # Convert QuerySet into List of Dictionaries
      print(permissions)
      # accessLevels = AccessLevel.objects.all().values()
      accessLevels = AccessLevel.objects.all().prefetch_related('permissions')
      print("access levels ====> : \n", accessLevels.values())
      accessLevels_json = json.loads(serializers.serialize('json', accessLevels))
      print("Access Levels JSON ====> : \n", accessLevels_json)
      accessLvls = [] 
      for al in accessLevels:
        new_lvl = {
          'id': al.id,
          'access': al.access,
          'permissions': [perm.permission for perm in al.permissions.all()], # al['fields']['permissions'],
          'users': list(al.users.values_list('last_name', flat=True)),
        }
        accessLvls.append(new_lvl)
      print("access levels ====> : \n", accessLvls)
      # access_dict = [access for access in accessLvls] # Convert QuerySet into List of Dictionaries
      context = {
        'Edit Permissions': {
          'columns': get_settings_columns(permissions[0]),
          'data': permission_dict,
          'model': 'Permission'
        },
        'Edit Access Levels': {
          'columns': get_settings_columns(accessLvls[0]),
          'data': accessLvls,
          'model': 'AccessLevel',
          'options': get_access_options(),
        },
      }
      # Return the data as JSON
      return JsonResponse(context)
  except Exception as e:
    return trace_error(e, True)
  
# def get_settings_columns(data):
#   # print(data)
#   headers = []
#   for key, value in data.items():
#     if 'id' not in key:
#       transformed_key = key.replace('_', ' ').title()
#       type = "text"
#       if 'time' in key:
#         type = "time"
#       if 'color' in key:
#         type = "color"
#       if 'description' in key:
#         type = "textarea"
#       if 'id' in key or 'name' in key:
#         type = "fixed"
#       headers.append({
#         "name": key,
#         "label": transformed_key,
#         "field": key,
#         "sortable": True,
#         "align": 'left',
#         "type": type
#       })
#   # print(headers)
#   return headers
  
def save_user_profile(data, model=None, id=None):
  print('form data ====> : \n \n', id, '\n', model, '\n', data)
  user = User.objects.get(id=id)
  print(user.id)
  if model['model'] == 'User':
    instance = user
    for key, value in data.items():
      setattr(instance, key, value)
      instance.save()
  else:
    print('model: ', model['model'])
    if not all(value in {None, ''} for value in data.values()):
      if model['model'] == 'Address':
        try:
          address = Address.objects.get(user=user)
        except Address.DoesNotExist:
          address = Address.objects.create(user=user)
        address.street = data['street']
        address.street2 = data['street2']
        address.apt_num = data['apt_num']
        address.save()
      elif model['model'] == 'CityState':
        print(data['zipcode'])
        try:
          city_state = CityState.objects.get(user=user)
          city_state.city = data['city']
          city_state.state = data['state']
          city_state.zipcode = data['zipcode']
          city_state.save()
        except CityState.DoesNotExist:
          city_state = CityState.objects.create(
            user=user,
            city = data['city'],
            state = data['state'],
            zipcode = data['zipcode']
          )
        city_state.save()
      elif model['model'] == 'Occupation':
        try:
          occupation = Occupation.objects.get(user=user)
          occupation.occupation = data['occupation']
          occupation.save()
        except Occupation.DoesNotExist:
          occupation = Occupation.objects.create(user=user, occupation=data['occupation'])
      elif model['model'] == 'AccessLevel':
        print('access: ', data['access'])
        try:
          print('User: ', user.id, user.first_name, user.last_name)
          check_access = AccessLevel.objects.filter(users__id=user.id).first()
          if data['access'] != '':
            if check_access:
              print('check_access: ', check_access)
              check_access.users.remove(user)
            else:
              print('No access found')
            access = AccessLevel.objects.get(
              id=data['access'],
            )
            print('access: ', access)
            access.users.add(user)
        except AccessLevel.DoesNotExist:
          print("AccessLevel.DoesNotExist")
          # occupation = Occupation.objects.create(user=user, occupation=data['occupation'])
  return

# ==================== NOTE: MAY NOT BE USED ========================
# @csrf_exempt
# def login2(request, login_form = Login_Form()):
#   if request.method == 'POST':
#     print(request.POST)
#     form = Login_Form(request.POST)
#     if form.is_valid():
#       print("it worked!")
#       # email = form.cleaned_data['email']
#       # password = form.cleaned_data['password']
#       # print(email, password )
#       # user = validate_login(email, password)
#       user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
#       # print('auth worked')
#       # print(user)
#       login(request, user)
#       # if user is not None:
#       #   # login(request, user)
#       #   return HttpResponseRedirect('/users/')
#       # else:
#       #   # Show an error message
#       pass

#   else:
#       login_form = Login_Form()
#   context = {
#     'login_form': login_form,
#     'page_title': 'Login Form'   
#   }
#   return render(request, 'login_copy.html', context)
#   # return JsonResponse({'form': login_form.as_table()})


# @csrf_exempt
# def validate(request):
#   print("made it to validate")
#   if request.method != "POST":
#     return redirect("login")
#   # print(request.method)
#   body = json.loads(request.body)
#   # print(bcrypt.hashpw(body['password'].encode(), bcrypt.gensalt()).decode())
#   # print(body['email'], User.objects.filter(email=body['email']))
#   if not len(User.objects.filter(email=body['email'])) > 0:
#     return HttpResponseBadRequest('Invalid Email')
#   else:
#     stored_data = User.objects.get(email=body['email'])
#     if not bcrypt.checkpw(body['password'].encode(), stored_data.password.encode()):
#       return HttpResponseBadRequest('Invalid Email or Password')
#   return JsonResponse({ 'response' : "All good!"})


# @ensure_csrf_cookie
# def get_csrf(request):
#   token = csrf.get_token(request)
#   return JsonResponse({'token' : token})

# def get_user_data(request, user_id, admin=False):
#   # print(user_id)
#   # if req["admin"] == "true":
#   # Fetch the user
#   user = get_object_or_404(User, pk=user_id)
#   data = {
#     'first_name': { 'type': 'input', 'value': user.first_name},
#     'middle_name': { 'type': 'input', 'value': user.middle_name},
#     'last_name': { 'type': 'input', 'value': user.last_name},
#     'email': { 'type': 'input', 'value': user.email},
#     'phone_number': { 'type': 'tel', 'value': user.phone_number},
#     'phone_type': { 'type': 'select', 'value': user.phone_type},
#     'nickname': { 'type': 'input', 'value': user.nickname},
#   }
#   for key in data:
#     if key in FORM_FIELD_LABELS:
#       data[key]['label'] = FORM_FIELD_LABELS[key]
  
#   options = get_form_options()
#   context = {
#     'forms': {
#       'Basic Info': data,
#       'Address': get_user_address(user),
#       # 'Phone': get_user_phone(user),
#       'Occupation': get_user_occupation(user),
#     },
#     'options': options,
#   }
#   # Return the data as JSON
#   return JsonResponse(context)

# @csrf_exempt 
# @api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def create_user(request):
#   if request.method == 'POST':
#     try:
#       # data = request.POST.copy()
#       data = json.loads(request.body.decode("utf-8"))
#       # data = data[0]['Basic Info']
#       data = list(data[0].values())[0]
#       print(data)
#       if not User.objects.filter(email__icontains=data['email']):
#         phone_number = data['phone_number']
#         if isinstance(phone_number, str):
#           phone_number = re.sub('\D', '', phone_number)
#         user, created = User.objects.update_or_create(
#           username=data['email'],
#           initials = get_unique_initials(data['first_name'], data['middle_name'], data['last_name']),
#           defaults={
#             'first_name': data['first_name'],
#             'middle_name': data['middle_name'],
#             'last_name': data['last_name'],
#             'email': data['email'],
#             'phone_number': phone_number,
#             'phone_type': data['phone_type'],
#             'nickname': data['nickname'],
#           }
#         )
#         if created:
#           generate_password(user)
#         return JsonResponse({'message':'New User Successfully Added'}, status=200)
#       print("Email already exists")
#       return JsonResponse({'message':'Email already exists'}, status=500)
#     except Exception as e:
#       return trace_error(e, True)
#   else:
#     user_form = UserInfoForm()
#     form = set_form_fields(user_form)
#     context = {
#       'forms': {
#         'Basic Info': form, 
#       },
#       'options': get_form_options(),
#     }
#     # return render(request, 'multiForm.html', context)
#     return JsonResponse(context)
#   print("something went wrong")
#   return JsonResponse({'message':'Something went wrong'}, status=500)

# def create_user_new(content):
#   try:
#     # data = request.POST.copy()
#     data = content
#     # data = data[0]['Basic Info']
#     # data = list(data[0].values())[0]
#     print(data)
#     data['middle_name'] = data.get('middle_name', '')
#     if not User.objects.filter(email__icontains=data['email']):
#       phone_number = data['phone_number']
#       if isinstance(phone_number, str):
#         phone_number = re.sub('\D', '', phone_number)
#       user, created = User.objects.update_or_create(
#         username=data['email'],
#         initials = get_unique_initials(data['first_name'], data['middle_name'], data['last_name']),
#         defaults={
#           'first_name': data['first_name'],
#           'middle_name': data['middle_name'],
#           'last_name': data['last_name'],
#           'email': data['email'],
#           'phone_number': phone_number,
#           'phone_type': data['phone_type'],
#           # 'nickname': data['nickname'],
#         }
#       )
#       if created:
#         generate_password(user)

#       return JsonResponse({'message':'New User Successfully Added'}, status=200)
#     print("Email already exists")
#     return JsonResponse({'message':'Email already exists'}, status=500)
#   except Exception as e:
#     return trace_error(e, True)