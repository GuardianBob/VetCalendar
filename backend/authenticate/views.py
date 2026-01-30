from django.shortcuts import render
from django.contrib.auth import authenticate
import requests, json, csv, os, pytz, argparse, logging, logging.handlers, sys, traceback, re
from django.http import JsonResponse, HttpResponse
import datetime, jwt
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict
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
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from logger.db_logger import DatabaseLogging
from Crypto.Cipher import AES
import base64
import hashlib

from .models import User, Address, CityState, Phone, AccessLevel, Permission, Occupation, AccountRequest
from .scripts import generate_password, get_settings_columns
from backend.utils import trace_error, send_html_email


logger = DatabaseLogging(__name__)

def trace_error(e, log=True):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	# tb = traceback.extract_tb(exc_traceback)
	filename, line_number, func_name, text = traceback.extract_tb(exc_traceback)[0]
	# filename, line_number, func_name, text = tb[-1]
	error_message = f"An error occurred in file {filename} on line {line_number} in {func_name}(): {text}"
	if log:
		logger.error(error_message)
		logger.error(f"Error: {str(e)}")
	print(f"{filename}:{line_number}: Error in {func_name}(): {text}")
	print(f"Error: {str(e)}")

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

@csrf_exempt
def user_login(request):
  try:
    if request.method == 'POST':
      content = request.POST
      print(content['email'])
      identifier = content['email']
      password = content['password']
      user = authenticate(request, username=identifier, password=password)
      if user is None:
        # Try to find user by email if not found by username
        User = get_user_model()
        try:
          user_obj = User.objects.get(email=identifier)
          user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
          user = None
      print(user)
      if user is not None:        
        login(request, user)
        # print(f'groups: {user.groups.all()}')
        is_admin = user.groups.filter(name='admin').exists()
        # print(f'is_admin: {is_admin}, {user.groups.filter(name='admin').values()}')
        RefreshToken.lifetime = timedelta(days=15)
        # Generate JWT token:
        refresh = RefreshToken.for_user(user)
        refresh['user_id'] = user.id
        refresh['admin'] = is_admin
        return JsonResponse({
          'refresh': str(refresh),
          'access': str(refresh.access_token),
          'admin': is_admin
        }, status=200)
      else:
        # return response_msg(400, 'Incorrect Login or Password')
        return JsonResponse({"message":'Incorrect Login or Password'}, status=400)
    # return JsonResponse({'form': login_form.as_table()})
  except Exception as e:
    return trace_error(e, True)

@csrf_exempt 
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def validate(request):
  try:
    if request.method == 'POST':
      if request.user.is_authenticated:
        user_access = AccessLevel.objects.filter(users=request.user).values('access', 'permissions__permission')
        access = list(map(lambda x: x['access'], user_access))
        access = list(set(access))
        permissions = list(map(lambda x: x['permissions__permission'], user_access))
        return JsonResponse({'message':'User Valid', 'access': access, 'permissions': permissions}, status=200)
    return JsonResponse({'message':'User is not validated', 'access': False}, status=400)
  except Exception as e:
    return trace_error(e, True)
  
@csrf_exempt 
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_password(request):
  try:
    if request.method == 'POST':
      content = request.POST
      # print(content['password'])
      if request.user.is_authenticated:
        User = get_user_model()
        user = User.objects.get(username=request.user)
        # print(user)
        decrypted_text = decrypt(content['password'])
        # print(f"decrypted: {decrypted_text}")
        if user is not None:
          user.set_password(decrypted_text)
          user.save()
          return JsonResponse({'message':'Password Updated'}, status=200)
        else:
          return JsonResponse({"message":'Unable to update password'}, status=400)
    return JsonResponse({'message':'User is not validated', 'access': False}, status=400)
  except Exception as e:
    return trace_error(e, True)
  
def decrypt(encrypted_text):
  try:
    secret_key = os.getenv('CRYPTO_KEY')
    if not secret_key:
      raise ValueError("Secret key not found in environment variables")
    print(f"Secret Key: {secret_key}")

    # Decode the base64 encoded ciphertext
    encrypted_bytes = base64.b64decode(encrypted_text)
    print(f"Encrypted Bytes: {encrypted_bytes}")

    # Extract the salt
    salt = encrypted_bytes[:16]
    actual_ciphertext = encrypted_bytes[16:]
    # print(f"Salt: {salt}")
    # print(f"Actual Ciphertext: {actual_ciphertext}")

    # Derive the key and IV using the salt and secret key
    key_iv = hashlib.pbkdf2_hmac('sha256', secret_key.encode(), salt, 10000, dklen=32 + 16)
    key = key_iv[:32]
    iv = key_iv[32:]
    # print(f"Derived Key: {key}")
    # print(f"Derived IV: {iv}")

    # Create the AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext
    decrypted_bytes = cipher.decrypt(actual_ciphertext)
    # print(f"Decrypted Bytes (before unpadding): {decrypted_bytes}")

    # Remove padding (PKCS7)
    padding_length = decrypted_bytes[-1]
    if padding_length > 16:
      raise ValueError("Invalid padding length")
    decrypted_bytes = decrypted_bytes[:-padding_length]
    # print(f"Decrypted Bytes (after unpadding): {decrypted_bytes}")

    # Convert bytes to string
    decrypted_text = decrypted_bytes.decode('utf-8')
    # print(f"Decrypted Text: {decrypted_text}")

    return decrypted_text
  except Exception as e:
    return trace_error(e, True)


# Helper function for unique initials
def get_unique_initials(first_name='', middle_name='', last_name=''):
  initials = first_name[0].upper() + last_name[0].upper()
  if middle_name:
    initials = first_name[0].upper() + middle_name[0].upper() + last_name[0].upper()
  if User.objects.filter(initials=initials).count() > 0:
    count = 1
    while User.objects.filter(initials=initials+str(count)).count() > 0:
      count += 1
    initials = initials+str(count)
  return initials


@csrf_exempt
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_list(request):
    try:
        users = User.objects.all().values('id', 'first_name', 'last_name', 'initials', 'email')
        user_list = list(users)
        return JsonResponse(user_list, safe=False)
    except Exception as e:
        return trace_error(e, True)


@csrf_exempt 
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
  try:
    if request.method == 'POST':
      email = request.body.decode("utf-8")
      try:
        user = model_to_dict(User.objects.prefetch_related('user_phone').get(email=email))
        address = model_to_dict(Address.objects.get(user=user["id"])) if Address.objects.filter(user=user["id"]).count() > 0 else None
        city_state = model_to_dict(CityState.objects.get(user=user["id"])) if CityState.objects.filter(user=user["id"]).count() > 0 else None
        occupation = model_to_dict(Occupation.objects.get(user=user["id"])) if Occupation.objects.filter(user=user["id"]).count() > 0 else None
        
        # Remove sensitive fields
        del user['password']
        del user['groups']
        del user['is_superuser']
        del user['is_staff']
        del user['is_active']
        del user['date_joined']
        del user['last_login']
        del user['user_permissions']

        user_info = {**user, **(address if address is not None else {}), **(city_state if city_state is not None else {}), **(occupation if occupation is not None else {})}
        user_json = json.dumps(user_info, default=str)
        return HttpResponse(user_json)
      except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)
  except Exception as e:
    return trace_error(e, True)


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
  try:
    if request.method == 'POST':
      data = json.loads(request.body)
      
      user = User.objects.get(id=data['user'])
      user.username = data['email']
      user.first_name = data['first_name']
      user.middle_name = data['middle_name']
      user.last_name = data['last_name']
      user.email = data['email']
      user.initials = data['initials'] if 'initials' in data else ''
      user.nickname = data['nickname'] if 'nickname' in data else ''
      user.save()
      
      if user.initials == '' and user.first_name != '' and user.last_name != '':
        initials = get_unique_initials(user.first_name, user.middle_name, user.last_name)
        user.initials = initials
        user.username = user.email
        user.save()

      # Create or update Address
      if 'street' in data:
        address, created = Address.objects.update_or_create(
          user=user,
          defaults={
            'street': data['street'],
            'street2': data['street2'],
            'apt_num': data['apt_num'],
          }
        )

      # Create or update CityState
      if 'state' in data:
        city_state, created = CityState.objects.update_or_create(
          user=user,
          defaults={
            'city': data['city'],
            'state': data['state'],
            'zipcode': data['zipcode'],
          }
        )

      # Create or update Phone
      if 'phone_number' in data:
        phone_number = re.sub('\D', '', data['phone_number'])
        if Phone.objects.filter(users__id=user.id).exists():
          phone = Phone.objects.get(users__id=user.id)
          phone.phone_number = phone_number
          phone.phone_type = data['phone_type']
          phone.save()
        else:
          phone, created = Phone.objects.update_or_create(
            defaults={
              'phone_number': phone_number,
              'phone_type': data['phone_type'],
            }
          )
          phone.users.add(user)
        
      # Create or update Occupation
      if 'occupation' in data:
        occupation, created = Occupation.objects.update_or_create(
          user=user,
          defaults={
            'occupation': data['occupation'],
          }
        )

      return JsonResponse({'message': 'User updated', 'user': user.username}, status=200)
  except Exception as e:
    return trace_error(e, True)


@csrf_exempt 
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_user_password(request):
  try:
    if request.method == 'POST':
      data = json.loads(request.body)
      user = User.objects.get(email=data['email'])
      if check_password(data['new_password'], user.password):
        return JsonResponse({'message':'New password cannot be the same as the old password'}, status=500)
      if check_password(data['old_password'], user.password):
        user.set_password(data['new_password'])
        user.save()
      else:
        return JsonResponse({'message':'Password is incorrect'}, status=500)
      return JsonResponse({'message': 'Password updated'}, status=200)
  except Exception as e:
    return JsonResponse({'message':'Something went wrong'}, status=500)


@csrf_exempt 
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def password_reset(request):
  try:
    if request.method == 'POST':
      data = json.loads(request.body)
      user = User.objects.get(email=data['email'])
      password = generate_password(user)
      message = f'''
        <p>Your password has been reset.</p>
        <p>Your temporary password is: <strong>{password['decrypted']}</strong></p>
      '''
      send_html_email("VSS Password Reset", message, [user.email])
      return JsonResponse({'message': 'Password reset'}, status=200)
  except Exception as e:
    return JsonResponse({'message':'Something went wrong'}, status=500)


@csrf_exempt 
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
  try:
    content = json.loads(request.body)
    user = User.objects.get(id=content['id'])
    user.delete()
    return JsonResponse({'message': 'User deleted'}, status=200)
  except Exception as e:
    return trace_error(e, True)
