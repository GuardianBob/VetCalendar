from django.urls import path
from . import views

urlpatterns = [
    path('get_csrf', views.get_csrf, name='get_csrf'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('return_user_list', views.return_user_list, name='return_user_list'),
    path('return_shifts', views.return_shifts, name='return_shifts'),
    path('return_shifts_old', views.return_shifts_old, name='return_shifts_old'),
    path('quick_add', views.quick_add, name='quick_add'),
    path('schedule_settings', views.schedule_settings, name='schedule_settings'),
]