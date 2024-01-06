from .models import User, UserPass, Address, CityState, Phone, AccessLevel, UserPrivileges, Occupation
from django import forms
import datetime
import bcrypt


STATE_SELECT = (
    ('', ''),
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AS', 'American Samoa'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('GU', 'Guam'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('MP', 'Northern Mariana Islands'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('PR', 'Puerto Rico'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VI', 'Virgin Islands'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming')
)

FORM_FIELDS = {
    "first_name": "First Name",
    "middle_name": "Middle Name",
    "last_name": "Last Name",
    "email": "E-Mail",
    "phone": "Phone Number",
    "address": "Address",
    "address_line2": "Address Line 2",
    "apt_num": "Apt #",
    "city": "City",
    "state": "State",
    "zipcode": "Zip Code",
    "password": "Password",
    "verify_password": "Verify Password",
}

class Register_Form(forms.Form):
  first_name = forms.CharField(max_length=200, widget=forms.TextInput, required=True)
  last_name = forms.CharField(max_length=200, widget=forms.TextInput, required=True)  
  email = forms.EmailField(max_length=200, widget=forms.EmailInput, required=True)
  address = forms.CharField(max_length=150, widget=forms.TextInput, required=False)
  address_line2 = forms.CharField(max_length=150, widget=forms.TextInput, required=False)
  apt_num = forms.CharField(max_length=10, widget=forms.TextInput, required=False)
  city = forms.CharField(max_length=35, widget=forms.TextInput, required=False)
  state = forms.ChoiceField(widget=forms.Select, choices=STATE_SELECT, required=False)
  zipcode = forms.IntegerField(widget=forms.TextInput, required=False)
  password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=True)
  verify_password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=True)

  def __init__(self, *args, **kwargs):
    super(Register_Form, self).__init__(*args, **kwargs)
    self.fields = set_attributes(self.fields)

  def clean(self):
    super(Register_Form, self).clean()
    first_name = self.cleaned_data.get('first_name')
    last_name = self.cleaned_data.get('last_name')
    email = self.cleaned_data.get('email')
    address = self.cleaned_data.get('address')
    address_line2 = self.cleaned_data.get('address_line2')
    apt_num = self.cleaned_data.get('apt_num')
    city = self.cleaned_data.get('city')
    state = self.cleaned_data.get('state')
    zipcode = self.cleaned_data.get('zipcode')
    # password = self.cleaned_data.get('password')
    # verify_password = self.cleaned_data.get('verify_password')

class Login_Form(forms.Form): 
    email = forms.EmailField(max_length=200, widget=forms.EmailInput)
    password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
      super(Login_Form, self).__init__(*args, **kwargs)
      self.fields = set_attributes(self.fields)

class UserCreationForm(forms.Form):
  first_name = forms.CharField(max_length=200, widget=forms.TextInput, required=True)
  middle_name = forms.CharField(max_length=200, widget=forms.TextInput, required=False)
  last_name = forms.CharField(max_length=200, widget=forms.TextInput, required=True)  
  email = forms.EmailField(max_length=200, widget=forms.EmailInput, required=True)
  phone = forms.CharField(max_length=200, widget=forms.TextInput, required=True)

  def __init__(self, *args, **kwargs):
    super(UserCreationForm, self).__init__(*args, **kwargs)
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
    fields[name].label = ''
    if "password" in name:
      fields[name].widget.attrs.update({
        'type': 'password',
      })
    if "email" in name:
      fields[name].widget.attrs.update({
      'type': 'email',
    })
  return fields