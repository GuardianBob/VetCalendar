from django import forms
import datetime
import re
from .models import ShiftName, ShiftType, Shifts, Calendar
from .scripts import convert_label

FORM_FIELDS = {
  'user': 'User',
  'shift': 'Shift',
  'shift_type': 'Shift Type',
  'shift_date': 'Shift Date',
  'shift_name': 'Shift Name',
  'shift_label': 'Shift Label',
  'start_time': 'Start Time',
  'end_time': 'End Time',
}

class QuickAddForm(forms.Form):
  user = forms.ChoiceField(widget=forms.Select, required=True)
  shift = forms.ChoiceField(widget=forms.Select, required=True)
  shift_type = forms.ChoiceField(widget=forms.Select, required=True)
  shift_date = forms.DateField(required=True)

  def __init__(self, *args, **kwargs):
      super(QuickAddForm, self).__init__(*args, **kwargs)
      self.fields = set_attributes(self.fields)

class ShiftNameForm(forms.ModelForm):
  class Meta:
    model = ShiftName
    fields = ['shift_name', 'shift_label', 'start_time', 'end_time']
    widgets = {
      'start_time': forms.TimeInput(attrs={'type': 'time'}),
      'end_time': forms.TimeInput(attrs={'type': 'time'}),
    }

  def __init__(self, *args, **kwargs):
    super(ShiftNameForm, self).__init__(*args, **kwargs)
    self.fields = set_attributes(self.fields)

class ShiftTypeForm(forms.ModelForm):
  class Meta:
    model = ShiftType
    fields = ['shift_type', 'shift_color', 'type_label']
    widgets = {
      'shift_type': forms.TextInput(attrs={'type': 'text'}),
      'shift_color': forms.TextInput(attrs={'type': 'color'}),
      'shift_label': forms.TextInput(attrs={'type': 'text'}),
    }

  def __init__(self, *args, **kwargs):
    super(ShiftTypeForm, self).__init__(*args, **kwargs)
    self.fields = set_attributes(self.fields)

def set_attributes(fields):
  # print(fields.keys())
  for name in fields.keys():
    # print("form: ", name)
    fields[name].widget.attrs.update({
      'class' : 'form-control input-field',
      'id' : name,
      'placeholder': set_label(name),
    })
    if name == 'phone_number':
      fields[name].widget.attrs.update({
        # 'pattern' : '([0-9]{3}) [0-9]{3}-[0-9]{4}',
        'title' : 'Please enter numeric digits only.'
      })
    fields[name].label = ''
  return fields

def set_label(label):
  try :
    return str(FORM_FIELDS[label])
  except:
    return convert_label(label)
    