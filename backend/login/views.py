from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from .models import User, Address, CityState, Phone, AccessLevel, UserPrivileges, Occupation, User_Info
from django.db.models import Prefetch, Q
from django.contrib import messages
from django.contrib.auth import logout
import bcrypt, json
from django.middleware import csrf
from .forms import Register_Form, Login_Form, UserCreationForm, UserAdminUpdateForm, UpdatePasswordForm, UpdateOccupationForm, UserInfoForm, AddressForm, CityStateForm, PhoneForm, EmailForm
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.forms.models import model_to_dict
import random, secrets, re, traceback, sys
from itertools import count
from django.contrib.auth import authenticate, login
from django.conf import settings
from datetime import timedelta
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

# Create your views here.
@csrf_exempt
def user_login(request):
  if request.method == 'POST':
    req = request.POST
    form = Login_Form(req)
    remember_me = req['remember_me']
    # print(remember_me)
    # print(form)
    if form.is_valid():
      # print("it worked!")
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      # user = validate_login(email, password)
      user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
      # print(user)
      if user is not None:
        login(request, user)
        # Generate JWT token:
        # refresh = TokenObtainPairSerializer.get_token(user)
        if remember_me:
          # Set refresh token lifetime to 30 days if "Remember Me" is checked
          RefreshToken.lifetime = timedelta(days=30)
        else:
          # Otherwise, set it to 1 day
          RefreshToken.lifetime = timedelta(days=1)

        # Generate JWT token:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
          'refresh': str(refresh),
          'access': str(refresh.access_token),
        }, status=200)
      else:
        # return response_msg(400, 'Incorrect Login or Password')
        return JsonResponse({"message":'Incorrect Login or Password'}, status=400)
    else:
      # print("failed")
      return JsonResponse({'message':'Incorrect Login or Password'}, status=400)
  else:
    form = Login_Form()
    context = {
      'form': form,
      'page_title': 'User Login:'   
    }
    return render(request, 'form.html', context)
  # return JsonResponse({'form': login_form.as_table()})


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
def create_user(request):
  if request.method == 'POST':
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
    user_form = UserInfoForm(request.POST)
    phone_form = PhoneForm(request.POST)
    # email_form = EmailForm(request.POST)
    # address_form = AddressForm(request.POST)
    # city_state_form = CityStateForm(request.POST)
    print(user_form.is_valid(), phone_form.is_valid())
    if user_form.is_valid() and phone_form.is_valid(): #and address_form.is_valid() and city_state_form.is_valid() 
      if not User.objects.filter(email__icontains=user_form.cleaned_data["email"]):
        user = user_form.save()
        phone = phone_form.save()
        phone.users.add(user)
        phone.save()
        # email = email_form.save(commit=False)
        # email.user = user
        # email.save()
        # address = address_form.save(commit=False)
        # address.user = user
        # address.save()
        # city_state = city_state_form.save(commit=False)
        # city_state.user = user
        # city_state.save()
        # login(request, user)
        return JsonResponse({'message':'New User Successfully Added'}, status=200)
      return JsonResponse({'message':'Email already exists'}, status=500)
    return JsonResponse({'message':'Form is invalid'}, status=500)
  else:
    user_form = UserInfoForm()
    phone_form = PhoneForm()
    # email_form = EmailForm()
    # address_form = AddressForm()
    # city_state_form = CityStateForm()
    # form = UserCreationForm()

    context = {
      'forms': {
        '': user_form, 
        'Phone': phone_form,
        # 'E-Mail': email_form,
        # 'Address': address_form,
        # 'CityState': city_state_form,
      },
      'page_title': 'Create New User'
    }
    return render(request, 'multiForm.html', context)
  return JsonResponse({'message':'Something went wrong'}, status=500)

def verify_new_user(email):
  print(email)
  user = User.objects.filter(email__icontains=email)
  return user

def get_unique_initials(first_name='', middle_name='', last_name=''):
    user_initials = first_name[0] + last_name[0]
    user_full_initials = f"{first_name[0]}{middle_name[0]}{last_name[0]}" if middle_name else user_initials
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

def save_new_user(user):
  print(user["first_name"])
  # Create a new user  
  new_initials=get_unique_initials(user["first_name"], user["middle_name"], user["last_name"])
  new_user = User.objects.create(
      first_name=user["first_name"],
      middle_name=user["middle_name"],
      last_name=user["last_name"],
      email=user["email"],
      initials=new_initials.upper()
  )  
  # Create a new user password
  new_password=generate_password()
  new_user_password = UserPass.objects.create(
      user=new_user,
      password=new_password["encrypted"],
      pw_reset = True,
      pw_reset_code = new_password["reset_code"]
  )  
  # Create a new phone for the new user
  new_phone = Phone.objects.create(
      number=re.sub('\D', '', user["phone"]),
      type=user["phone_type"],
  )
  # Add the new phone to the new user's phones
  new_phone.users.add(new_user)
  # Save all of these objects to the database
  # new_user.save()
  # new_user_password.save()
  # new_phone.save()
  user_info = {
    "user": new_user,
    "user_password": new_password['decrypted'],
    "user_phone": new_phone
  }
  return user_info

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

def generate_password(password_length=20):
  password = secrets.token_urlsafe(password_length)
  reset_code = secrets.token_urlsafe(50)
  # print(password)
  salted_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
  # print(salted_pass)
  new_password = {
    "decrypted" : password,
    "encrypted" : salted_pass,
    "reset_code": reset_code
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
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_list(request):
    print(request.META.get('HTTP_AUTHORIZATION'))
    print(request.session)
    users = User.objects.select_related('user_level').values('id', 'first_name', 'last_name', 'initials', 'email', 'user_level__name')
    print(users)
    user_dict = [user for user in users] # Convert QuerySet into List of Dictionaries
    user_data = json.dumps(user_dict)   
    print(user_data)
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

@csrf_exempt 
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    if request.method == 'GET':
      # req = json.loads(request.body.decode("utf-8"))
      req = request.GET
      # print(req["id"], req["admin"])
      print(req)
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
      if req["admin"] == "true":
        # profile = User.objects.filter(id=req["id"]).values(*fields_to_select)
        user = User.objects.get(id=req["id"])
        address = user.user_address if hasattr(user, 'user_address') else None
        city_state = user.user_city_state if hasattr(user, 'user_city_state') else None
        phone = user.user_phone.first() if hasattr(user, 'user_phone') else None
        occupation = user.user_occupation if hasattr(user, 'user_occupation') else None
      else:
        profile = User.objects.filter(id=req["id"]).values(*fields_to_select)
        print(profile[0])
      
      data = {
        'first_name': user.first_name,
        'middle_name': user.middle_name,
        'last_name': user.last_name,
        'initials': user.initials,
        'nickname': user.nickname,
        'email': user.email,
        'phone': phone.phone_number if phone else '',
        'phone_type': phone.phone_type if phone else '',
        'apt_num': address.apt_num if address else '',
        'address': address.street if address else '',
        'address_line2': address.street2 if address else '',
        'city': city_state.city if city_state else '',
        'state': city_state.state if city_state else '',
        'zipcode': city_state.zipcode if city_state else '',
        # 'occupation': occupation.name if occupation else '',
      }
      userDetails = UserAdminUpdateForm(data)
      updateOccupation = UpdateOccupationForm(occupation)
      context = {
        'forms': {
          'Details': userDetails, 
          # 'Update Password': updatePassword,
          'Occupation': updateOccupation,  
        },
        'page_title': 'Update User'
      }
      return render(request, 'multiForm.html', context)
    # return JsonResponse(profile[0])
    else:
      return update_user(request)

@csrf_exempt
def update_user(request):
  try:
    data = request.POST
    print(data)
    # Create or update User
    user, created = User.objects.update_or_create(
        initials=data['initials'],
        defaults={
            'first_name': data['first_name'],
            'middle_name': data['middle_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'occupation': data['occupation'],
        }
    )

    # Create or update Address
    if data['address'].strip():
      address, created = Address.objects.update_or_create(
          user=user,
          defaults={
              'street': data['address'],
              'street2': data['address_line2'],
              'apt_num': data['apt_num'],
          }
      )

      # Create or update CityState
      city_state, created = CityState.objects.update_or_create(
          user=user,
          defaults={
              'city': data['city'],
              'state': data['state'],
              'zipcode': data['zipcode'],
          }
      )

    # Create or update Address
    if data['phone'].strip():
      phone, created = Phone.objects.update_or_create(
          users=user,
          defaults={
              'number': data['phone'],
              'type': data['phone_type'],
          }
      )

    return JsonResponse({'message': 'User updated'}, status=200)
  except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    filename, line_number, func_name, text = traceback.extract_tb(exc_traceback)[0]
    print(f"An error occurred in file {filename} on line {line_number}")
    print(e)
    return JsonResponse({'message': 'an error occurred'}, status=500)

@csrf_exempt 
def get_user_profile2(request):
    req = json.loads(request.body.decode("utf-8"))
    # req = request.body
    # print(req["id"], req["admin"])
    print(req)
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
    if req["admin"] == "true":
      # profile = User.objects.filter(id=req["id"]).values(*fields_to_select)
      user = User.objects.get(id=req["id"])
      address = user.user_address if hasattr(user, 'user_address') else None
      city_state = user.user_city_state if hasattr(user, 'user_city_state') else None
      phone = user.user_phone.first() if hasattr(user, 'user_phone') else None
      occupation = user.user_occupation if hasattr(user, 'user_occupation') else None
    else:
      profile = User.objects.filter(id=req["id"]).values(*fields_to_select)
      print(profile[0])
    
    data = {
      'first_name': user.first_name,
      'middle_name': user.middle_name,
      'last_name': user.last_name,
      'initials': user.initials,
      'nickname': user.nickname,
      'email': user.email,
      'phone': phone.number if phone else '',
      'phone_type': phone.type if phone else '',
      'apt_num': address.apt_num if address else '',
      'address': address.street if address else '',
      'address_line2': address.street2 if address else '',
      'city': city_state.city if city_state else '',
      'state': city_state.state if city_state else '',
      'zipcode': city_state.zipcode if city_state else '',
      'occupation': occupation.name if occupation else '',
    }
    userDetails = UserAdminUpdateForm(data)
    updatePassword = UpdatePasswordForm()
    
    context = {
      'forms': {
        'Details': userDetails, 
        'Update Password': updatePassword, 
      },
      'page_title': 'Update User'
    }
    return render(request, 'multiForm.html', context)
    # return JsonResponse(profile[0])