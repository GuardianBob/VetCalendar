from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('token/verify/', views.validate_token, name='validate_token'),
  path('', views.user_login, name='user_login'),
  path('validate', views.validate, name='validate'),  
  path('update_password', views.update_user_password, name='update_password'),
  path('reset_password', views.password_reset, name='reset_password'),
  path('get_user_list', views.get_user_list, name='get_user_list'),
  path('get_user_profile', views.get_user_profile, name='get_user_profile'),
  path('update_profile', views.update_profile, name='update_profile'),
  path('delete_user', views.delete_user, name='delete_user'),
]