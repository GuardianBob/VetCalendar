from django.urls import path
from . import views

urlpatterns = [
    path('get_csrf', views.get_csrf, name='get_csrf'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('calendar/test', views.calendar_test, name='calendar_test'),
    path('calendar/test_event', views.event_test, name='event_test'),
    path('return_user_list', views.return_user_list, name='return_user_list'),
    path('return_shifts', views.return_shifts, name='return_shifts'),    
    path('quick_add', views.quick_add, name='quick_add'),
]