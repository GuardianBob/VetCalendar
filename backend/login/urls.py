from django.urls import path
from . import views

urlpatterns = [
    # path('', views.login2),
    path('', views.login, name='login'),
    path('login2', views.login2, name='login2'),
    path('validate', views.validate, name='validate'),
    path('get_csrf', views.get_csrf, name='get_csrf'),
    path('register', views.register, name="register"),
    path('add_user', views.add_user, name="add_user"),
    path('get_user_profile', views.get_user_profile, name='get_user_profile'),
    path('get_user_list', views.get_user_list, name='get_user_list'),
    path('create_user', views.create_user, name='create_user'),
    path('forms_page', views.login, name='login'),
    # path('user_register', views.new_registration, name='user_register'),
    # path('add_user', views.add_new_user, name='add_user'),
    # path('user_validate', views.validate_login),
    # path('logout', views.logout_view, name='logout'),
    ]