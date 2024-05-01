from django.http import JsonResponse, HttpResponse
from VetCalendar.models import FormBuilderNew
import datetime, json, traceback, sys, re, pytz, os
from dateutil.parser import parse
from django.apps import apps
from importlib import import_module
import logging, inspect
import logging.handlers
from django.db import models
from django.core.mail import send_mail, EmailMultiAlternatives

# Create a logger
logger = logging.getLogger(__name__)

# Set the log level
logger.setLevel(logging.ERROR)

# Create a rotating file handler
handler = logging.handlers.RotatingFileHandler('logs/error.log', maxBytes=20000, backupCount=5)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

def trace_error(e, isForm=False):
  exc_type, exc_value, exc_traceback = sys.exc_info()
  filename, line_number, func_name, text = traceback.extract_tb(exc_traceback)[0]
  error_message = f"An error occurred in file {filename} on line {line_number} in {func_name}(): {text}"
  logger.error(error_message)
  logger.error("Error: ", e)
  print(f"An error occurred in file {filename} on line {line_number} in {func_name}(): {text}")
  print("Error: ", e)
  if isForm:
      return JsonResponse({'message':'Form is invalid'}, status=500)
  return JsonResponse({'message':'Something went wrong'}, status=500)

def print_line(extra_text=None):
    frame_info = inspect.getframeinfo(inspect.currentframe().f_back)
    file_path = os.path.abspath(frame_info.filename)
    print("===================================== \n")
    print(f"File: file:///{file_path}:{frame_info.lineno}")
    print(f'\n {extra_text}')
    print("\n===================================== ")

def convert_label(name):
    name_with_spaces = re.sub('_', ' ', name)
    capitalized_name = name_with_spaces.title()
    return capitalized_name

def convert_to_shift_datetime(date, time):
  print(date, time)
  shift_date = parse(date).date()
  shift_datetime = datetime.datetime.combine(shift_date, time)
  # shift_datetime = fix_timezone(shift_datetime)
  return shift_datetime

def get_app_from_model(app_names, model_name):
  for app_name in app_names:
    try:
      apps.get_model(app_name, model_name)
      return app_name
    except LookupError:
      continue
  return None

def strip_form_content(content):
  fields = {}
  for field in content['fields']:
    print('field =====> : \n', field)
    # fields[key] = value['value'] if isinstance(value['value'], list) else value['value']['value']
    # if field['type'] == 'time':
    # print(field['value'], '=====>', parse(field['value']).time())
    #   field['value'] = datetime.strptime(field['value'], "%H%M").time()
    if isinstance(field['value'], list):
      print("List: ===>: ", field['value'])
      if field['type'] != 'date':
        field['value'] = [item['value']['option'] for item in field['value'] if 'option' in item['value']]
      # for item in field['value']:
      #   print("List_item: ===>: ", item['value'])
      #   if 'option' in item['value']:
      #     print("Option: ===>: ", item['value']['option'])
      #     item = item['value']['option']
    if isinstance(field['value'], dict):
      fields[field['field_name']] = field['value']['value']
    # elif isinstance(field['value'], list):
    #   fields[key] = value['value']
    else:
      fields[field['field_name']] = field['value']
    print('\n New Fields =====>: \n', fields)
  return fields

def pull_model_options(field_options):
  options = []
  for item in field_options:
    print(item)
    related_model_name = item.get('related_model')
    option_label = item.get('option_label')
    if related_model_name and option_label:
      app_name, model_name = related_model_name.split('.')
      related_model = apps.get_model(app_name, model_name)
      model_objects = related_model.objects.all()
      for obj in model_objects:
        option = {
          'field': item['field'],
          'option': obj.id,
          'label': getattr(obj, option_label)
        }
        options.append(option)
  return options

def get_model_instance(app_name, model_name, id):
  try:
    print(f'Getting model instance for: \n app: {app_name} \n model: {model_name} \n id: {id}')
    Model = apps.get_model(app_name, model_name)
    instance = Model.objects.get(id=id)
    return instance
  except Model.DoesNotExist:
    return None

def get_model_values(app_name, model_name, id):
  try:
    print(f'Getting model instance for: \n app: {app_name} \n model: {model_name} \n id: {id}')
    Model = apps.get_model(app_name, model_name)
    instance = Model.objects.values().get(id=id)
    return instance
  except Model.DoesNotExist:
    return None
  
def get_linked_model_values(app_name, model_name, foreign_key, id):
  try:
    print(f'Getting M2M model instance for: \n app: {app_name} \n model: {model_name} \n foreign_key: {foreign_key}')
    Model = apps.get_model(app_name, model_name)
    instance = Model.objects.values().filter(**{foreign_key: id}).first()
    print("Linked Instance: ====> ", instance)
    return instance
  except Model.DoesNotExist:
    return None
  
def get_m2m_linked_model_values(app_name, model_name, foreign_key, id):
  try:
    print(f'Getting model instance for: \n app: {app_name} \n model: {model_name} \n foreign_key: {foreign_key}')
    Model = apps.get_model(app_name, model_name)
    instance = Model.objects.filter(foreign_key__id=id).values().first()  # Double underscore in 'foreign_key__id' allows filtering the realted model by the id given
    print("Linked Instance: ====> ", instance)
    return instance
  except Model.DoesNotExist:
    return None
  
def is_foreign_key(model, field_name):
  field_object = model._meta.get_field(field_name)
  return isinstance(field_object, models.ForeignKey)

def save_model(model, values, id=None):
  print(f'save_model: \n{model} \n{values} \n{id}')
  # try:
  Model = apps.get_model(model['app'], model['model'])
  permissions = values.pop('permissions', [])
  users = values.pop('users', [])
  for key, value in values.items():
    if is_foreign_key(Model, key):
      print(f"{key} is a ForeignKey.")
      value = get_model_values(model['app'], key.capitalize(), id)
      print("\n foreign key: \n", value)
  if id != None:
    print(' \n updating instance')
    instance = Model.objects.get(id=id)
    if permissions:
      instance.permissions.clear()
      instance.permissions.set(permissions)
    elif users:
      instance.users.clear()
      instance.users.set(users)
    else:
      # for permission in permissions:
      #   instance.permissions.add(permission)
      for key, value in values.items():
        setattr(instance, key, value)
      print(instance)
    instance.save()
  else:
    instance = Model(**values)
    instance.save()  
  if permissions:
    instance.permissions.set(permissions)
  if users:
    instance.users.set(users)
  # except Exception as e:
  #   return trace_error(e, True)  
    
def delete_model(model, id):
  print(f'delete_model: \n{model} \n{id}')
  # try:
  app_name = get_app_from_model(['VetCalendar', 'login'], model)
  Model = apps.get_model(app_name, model)
  if id != None:
    print(' \n deleting instance')
    # instance = Model.objects.values().get(id=id)
    # print(instance)
    instance = Model.objects.get(id=id)
    instance.delete()
  return
  # except Exception as e:
  #   return trace_error(e, True)  
    
def save_linked_model(model, values, id=None):
  print(f'save_model: \n{model} \n{values} \n{id}')
  # try:
  # Model = apps.get_model(model['app'], model['model'])
  # for key, value in values.items():
  #   if is_foreign_key(Model, key):
  #     print(f"{key} is a ForeignKey.")
  #     value = get_model_values(model['app'], key.capitalize(), id)
  #     print("\n foreign key: \n", value)
  # if id != None:
  #   print(' \n updating instance')
  #   instance = Model.objects.get(id=id)
  #   for key, value in values.items():
  #     setattr(instance, key, value)
  #   print(instance)
  #   instance.save()
  # else:
  #   instance = Model(**values)
  #   instance.save()  
  return
  # except Exception as e:
  #   return trace_error(e, True)
  
def get_function(app_name, function_name):
    module = import_module(f'{app_name}.views')
    print(module)
    function = getattr(module, function_name)
    print(function)
    return function
  
def fill_form(form, values):
  print("\n====LOADING====\n", form, "\n", values)
  for field in form['fields']:
    if field['type'] == 'date':
      field['value'] = values[field['model_edit_field']].strftime('%b-%d-%Y')
    elif field['field_name'] == 'foreign_key':
      f_key = field['model_edit_field']
      print("foreign key: ====> ", f_key)
      field['value'] = values[f'{f_key}_id']
    elif field['field_name'] == 'many_to_many':
      print("\n ============== \n    many to many: ====> \n =========== \n", values)
      field['value'] = values['access']
      print("\n field value: ====> \n", field['value'])
    #   # field['value'] = values[field['model_edit_field']] if field['model_edit_field'] in values else ''
    else:
      field['value'] = values[field['model_edit_field']] if field['model_edit_field'] in values else ''
    
  print("\n =====END LOADING====\n")
  return form

# NOTE:
# Forms should be sent in an array
# 

def process_forms_test(content): 
  try:
    # content = list(content[0].values())[0]
    # print('\n \n', content)
    if content['save'] == True:
      return save_form(content)
    else:
      return build_form(content)
  except Exception as e:
    return trace_error(e, True)
  
def build_form(content):
  try:
    print('trying the build')
    # if form != None:
    if content['forms'] != None:
      forms = []
      main_model = None
      linked_instance = None
      if 'linked' in content and content['linked'] == True and 'id' in content:
        print("Linked Item: ====> ", content['forms'][0])
        form_model = FormBuilderNew.objects.values('app', 'model').get(form_name=content['forms'][0])
        # print("Form Model: ====> ", form_model)
        main_model = form_model['model']
        # linked_instance = get_model_values(form_model['app'], form_model['model'], content['id'])
        # print("Linked Instance: ====> ", linked_instance)
      for form in content['forms']:
        # print(form)
        form = FormBuilderNew.objects.values().get(form_name=form)
        # print("FORM ====> \n", form)
        for value in form['fields']:
          if value['type'] == 'date':
            value['value'] = None if value['value'] == '' else value['value']
          if value['type'] == 'multi-select' or value['type'] == 'multi-text' or value['type'] == 'multi-select-text':
            value['value'] = [] if value['value'] == '' else value['value']
          if value['type'] == 'checkbox':
            if value['value'] == 'True' or value['value'] == 'true':
              value['value'] = True
            else:
              value['value'] = False
            # print(value)
        # print(form['app'], form['model'], form['save_function'])
        if "id" in content:
          values = None
          if 'linked' in content and content['linked'] == True and form['model'] != main_model:
            print(form)
            for field in form['fields']:
              if 'foreign_key' in field['field_name'] or 'many_to_many' in field['field_name']:
                print("foreign key: ====> ", field['model_edit_field'])
                values = get_linked_model_values(form['app'], form['model'], field['model_edit_field'], content["id"])
              elif 'many_to_many' in field['field_name']:
                print("many to many: ====> ", field['model_edit_field'])
                values = get_m2m_linked_model_values(form['app'], form['model'], field['model_edit_field'], content["id"])
          else:
            values = get_model_values(form['app'], form['model'], content["id"])
            # print(values)
          if values:
            form = fill_form(form, values)
            # function = globals()[form['save_function']]
            # form = function({'form': form, "values": values}, True)
            print("\n Saved Test: ====> \n", form)
        # Function to read form['field_options'] and pull model objects
        print("Field Options: ====> ", form['field_options'])
        options = pull_model_options(form['field_options'])
        options.extend(form['custom_options'])
        print("Updated Options: ====> ", options)
        forms.append({'title': convert_label(form['form_name']),
          "fields": form["fields"],
          'options': options,
          'model': { 'app': form['app'], 'model': form['model'] },
          'function': form['save_function'],
          'id': content["id"] if 'id' in content else None,
        })
        # context = {
        #   'forms': {
        #     convert_label(form['form_name']): {
        #       "fields": form["fields"],
        #       'options': options,
        #       'model': { 'app': form['app'], 'model': form['model'] },
        #       'function': form['save_function'],
        #       'id': id if id else None,
        #     }
        #   },
        # }
    context = { 'forms' : forms}
    print(context)
    return JsonResponse(context)
  except Exception as e:
    return trace_error(e, True)

def save_form(content):
  try:
    main_form = content['forms'][0]    
    print('first form =====> : \n', main_form)
    for form in content['forms']:
      print('\n ========== Attempting to save ========== \n')
      print(form)
      print(form['function'])
      print(form['model']['app'])
      form_values = strip_form_content(form)
      print(form_values)
      if 'linked' in content and content['linked'] == True:        
        save_function = get_function(main_form['model']['app'], main_form['function'])
        save_function(form_values, form['model'], main_form['id'])
        # save_linked_model(form['model'], form_values , main_form['id'])
      else:
        if form['function'] != None:
          save_function = get_function(form['model']['app'], form['function'])
          print('form ID =====> : ', form['id'])
          if form['id'] != None and form['id'] != '':
            return save_function(form_values, form['id'])
          else:
            return save_function(form_values)
        # function = globals()[form['function']]
        else:  
          if form['id'] != None or form['id'] != '':
            save_model(form['model'], form_values , form['id'])
          else:      
            save_model(form['model'], form_values, None)
    return JsonResponse({'message': main_form['title'] + f' Added/Updated'}, status=200)
  except Exception as e:
    return trace_error(e, True)
  
def send_text_email(subject, message, recipient_list):
  from_email = EMAIL_HOST_USER
  if os.getenv('DEVELOPMENT_MODE') == 'True':
    recipient_list = [os.getenv('DEBUG_EMAIL')]
  print(f'sending email to: {recipient_list}')
  send_mail(
      subject,
      message,
      from_email,
      recipient_list,
      fail_silently=False,
  )
  return

def send_html_email(subject, message, recipient_list, text_content=None):
  from_email = EMAIL_HOST_USER
  if os.getenv('DEVELOPMENT_MODE') == 'True':
    recipient_list = [os.getenv('DEBUG_EMAIL')]
  print(f'sending email to: {recipient_list}')
  msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
  msg.attach_alternative(message, "text/html")
  msg.send()
  return