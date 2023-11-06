from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import User
from django.contrib import messages
from django.contrib.auth import logout
import bcrypt
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
  print(request)
  return JsonResponse({ 'response' : "made it to validate"})

def get_csrf(request):
  token = csrf.get_token(request)
  return JsonResponse({'token' : token})