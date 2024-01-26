from django import forms
import datetime
import re
from .models import Shift, ShiftType, ScheduleShift, Calendar

FORM_FIELDS = {
  'user': 'User',
  'shift': 'Shift',
  'shift_type': 'Shift Type',
  'shift_date': 'Shift Date',
}

class QuickAddForm(forms.Form):
  user = forms.ChoiceField(widget=forms.Select, required=True)
  shift = forms.ChoiceField(widget=forms.Select, required=True)
  shift_type = forms.ChoiceField(widget=forms.Select, required=True)
  shift_date = forms.DateField(required=True)

  def __init__(self, *args, **kwargs):
      super(QuickAddForm, self).__init__(*args, **kwargs)
      self.fields = set_attributes(self.fields)

def set_attributes(fields):
  # print(fields.keys())
  for name in fields.keys():
    # print("form: ", name)
    fields[name].widget.attrs.update({
      'class' : 'form-control input-field',
      'id' : name,
      'placeholder': str(FORM_FIELDS[name]),
    })
    if name == 'phone_number':
      fields[name].widget.attrs.update({
        # 'pattern' : '([0-9]{3}) [0-9]{3}-[0-9]{4}',
        'title' : 'Please enter numeric digits only.'
      })
    fields[name].label = ''
  return fields