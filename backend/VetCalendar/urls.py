from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('get_csrf', views.get_csrf, name='get_csrf'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('return_user_list', views.return_user_list, name='return_user_list'),
    path('return_shifts', views.return_shifts, name='return_shifts'),
    # path('return_shifts_old', views.return_shifts_old, name='return_shifts_old'),
    # path('quick_add', views.quick_add, name='quick_add'),
    path('delete_event', views.delete_event, name='delete_event'),
    path('clear_shifts', views.clear_shifts, name='clear_shifts'),
    # path('save_schedule_updates', views.save_schedule_updates, name='save_schedule_updates'),
    re_path(r'^edit_event(?:/(?P<id>\d+))?$', views.edit_event, name='edit_event'),
    path('schedule_settings', views.schedule_settings, name='schedule_settings'),
    path('get_keys', views.get_keys, name='get_keys'),
    re_path(r'^get_model_form(?:/(?P<model>\w+))?$', views.get_model_form, name='get_model_form'),
    # re_path(r'^add_edit_form(?:/(?P<id>\d+))?$', views.form_builder, name='form_builder'),
    path('get_table_fields', views.get_table_fields, name='get_table_fields'),
    path('get_field_options', views.get_field_options, name='get_field_options'),
    re_path(r'^get_formbuilder_form(?:/(?P<form>\w+))?(?:/(?P<id>\w+))?$', views.get_formbuilder_form, name='get_formbuilder_form'),
    # path('add_json_form', views.add_json_form, name='add_json_form'),
    # path('test_json_form', views.test_json_form, name='test_json_form'),
    path('handle_forms', views.handle_forms, name='handle_forms'),
    path('test_email', views.test_email, name='test_email'),
]