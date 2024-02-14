from django.urls import path, re_path
from . import views
# from .views import UserListView

urlpatterns = [
    # path('', views.login2),
    path('', views.user_login, name='login'),
    path('login', views.login, name='login'),
    path('login2', views.login2, name='login2'),
    path('validate', views.validate, name='validate'),
    path('get_csrf', views.get_csrf, name='get_csrf'),
    path('register', views.register, name="register"),
    path('account_request', views.account_request, name="account_request"),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_profile/<int:id>', views.user_profile, name='user_profile'),
    path('get_user_data/<int:user_id>', views.get_user_data, name='get_user_data'),
    path('get_user_list', views.get_user_list, name='get_user_list'),
    path('create_user', views.create_user, name='create_user'),
    path('forms_page', views.login, name='login'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('admin_settings', views.admin_settings, name='admin_settings'),
    # path('get_test_form/<int:id>', views.get_test_form, name='get_test_form'),
    # path('submit_test_form', views.submit_test_form, name='submit_test_form'),
    # path('get_user_list', UserListView.as_view(), name='user_list'),
    # path('user_register', views.new_registration, name='user_register'),
    # path('add_user', views.add_new_user, name='add_user'),
    # path('user_validate', views.validate_login),
    # path('logout', views.logout_view, name='logout'),
    ]