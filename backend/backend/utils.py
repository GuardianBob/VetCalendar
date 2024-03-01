from django.http import JsonResponse, HttpResponse
from VetCalendar.models import FormBuilderNew
import datetime, json, traceback, sys, re, pytz, os
from dateutil.parser import parse as parse_date
from django.apps import apps
from importlib import import_module
import logging
import logging.handlers
from django.db import models

# Create a logger
logger = logging.getLogger(__name__)

# Set the log level
logger.setLevel(logging.ERROR)

# Create a rotating file handler
handler = logging.handlers.RotatingFileHandler('error.log', maxBytes=20000, backupCount=5)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

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

def convert_label(name):
    name_with_spaces = re.sub('_', ' ', name)
    capitalized_name = name_with_spaces.title()
    return capitalized_name

def convert_to_shift_datetime(date, time):
  print(date, time)
  shift_date = parse_date(date).date()
  shift_datetime = datetime.datetime.combine(shift_date, time)
  # shift_datetime = fix_timezone(shift_datetime)
  return shift_datetime

def strip_form_content(content):
  fields = {}
  for field in content['fields']:
    # print(field)
    # fields[key] = value['value'] if isinstance(value['value'], list) else value['value']['value']
    if isinstance(field['value'], dict):
      fields[field['field_name']] = field['value']['value']
    # elif isinstance(field['value'], list):
    #   fields[key] = value['value']
    else:
      fields[field['field_name']] = field['value']
    # print(fields)
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
    print(f'Getting model instance for: \n app: {app_name} \n model: {model_name} ')
    Model = apps.get_model(app_name, model_name)
    instance = Model.objects.values().filter(**{foreign_key: id}).first()
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
  for key, value in values.items():
    if is_foreign_key(Model, key):
      print(f"{key} is a ForeignKey.")
      value = get_model_values(model['app'], key.capitalize(), id)
      print("\n foreign key: \n", value)
  if id != None:
    print(' \n updating instance')
    instance = Model.objects.get(id=id)
    for key, value in values.items():
      setattr(instance, key, value)
    print(instance)
    instance.save()
  else:
    instance = Model(**values)
    instance.save()  
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
          if value['type'] == 'multi-select' or value['type'] == 'multi-text':
            value['value'] = [] if value['value'] == '' else value['value']
            # print(value)
        # print(form['app'], form['model'], form['save_function'])
        if "id" in content:
          values = None
          if 'linked' in content and content['linked'] == True and form['model'] != main_model:
            print(form)
            for field in form['fields']:
              if 'foreign_key' in field['field_name']:
                print("foreign key: ====> ", field['model_edit_field'])
                values = get_linked_model_values(form['app'], form['model'], field['model_edit_field'], content["id"])
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
            save_function(form_values, form['id'])
          else:
            save_function(form_values)
        # function = globals()[form['function']]
        else:  
          if form['id'] != None or form['id'] != '':
            save_model(form['model'], form_values , form['id'])
          else:      
            save_model(form['model'], form_values, None)
    return JsonResponse({'message': main_form['title'] + f' Added/Updated'}, status=200)
  except Exception as e:
    return trace_error(e, True)