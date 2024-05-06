from django.urls import path, re_path
from . import views
# from .views import UserListView

urlpatterns = [
    # path('', views.login2),
    path('', views.user_login, name='login'),
    path('login', views.login, name='login'),
    # path('login2', views.login2, name='login2'),
    path('validate', views.validate, name='validate'),
    # path('get_csrf', views.get_csrf, name='get_csrf'),
    path('register', views.register, name="register"),
    path('request_access', views.request_access, name="request_access"),
    re_path(r'^user_profile(?:/(?P<id>\d+))?$', views.user_profile, name='user_profile'),
    path('get_user_profile', views.get_user_profile, name='get_user_profile'),
    path('update_profile', views.update_profile, name='update_profile'),
    # path('get_user_data/<int:user_id>', views.get_user_data, name='get_user_data'),
    path('get_user_list', views.get_user_list, name='get_user_list'),
    # path('create_user', views.create_user, name='create_user'),
    # path('forms_page', views.login, name='login'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('master_settings', views.master_settings, name='master_settings'),
    # path('submit_test_form', views.submit_test_form, name='submit_test_form'),
    # path('get_user_list', UserListView.as_view(), name='user_list'),
    # path('user_register', views.new_registration, name='user_register'),
    # path('add_user', views.add_new_user, name='add_user'),
    # path('user_validate', views.validate_login),
    # path('logout', views.logout_view, name='logout'),
    ]