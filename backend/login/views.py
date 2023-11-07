from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from .models import User
from django.contrib import messages
from django.contrib.auth import logout
import bcrypt, json
from django.middleware import csrf
from .forms import Register_Form, Login_Form
from django.views.decorators.csrf import csrf_exempt


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

def get_csrf(request):
  token = csrf.get_token(request)
  return JsonResponse({'token' : token})