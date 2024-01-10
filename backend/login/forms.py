from .models import User, UserPass, Address, CityState, Phone, AccessLevel, UserPrivileges, Occupation, FormOptions
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
    "initials": "Initials",
    "nickname": "Nickname",
    "email": "E-Mail",
    "phone": "Phone Number",
    "phone_type": "Phone Type",
    "address": "Address",
    "address_line2": "Address Line 2",
    "apt_num": "Apt #",
    "city": "City",
    "state": "State",
    "zipcode": "Zip Code",
    "password": "Password",
    "verify_password": "Verify Password",
    "occupation": "Occupation"
}

PHONE_TYPE = (
  ('mobile', 'Mobile'),
  ('home', 'Home'),
  ('work', 'Work'),
  ('other', 'Other')
)

class ProfileFields():
  user_fields = [f.name for f in User._meta.get_fields()]
  # userpass_fields = ['user_password__' + f.name for f in UserPass._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
  userpass_fields = ['user_password__password']
  address_fields = ['user_address__' + f.name for f in Address._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
  citystate_fields = ['user_city_state__' + f.name for f in CityState._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
  phone_fields = ['user_phone__' + f.name for f in Phone._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
  level_fields = ['user_level__' + f.name for f in AccessLevel._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
  privileges_fields = ['user_privileges__' + f.name for f in UserPrivileges._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]
  occupation_fields = ['user_occupation__' + f.name for f in Occupation._meta.get_fields() if f.name not in ['user', 'created_at', 'updated_at']]

def option_fields(field):
  form_options = FormOptions.objects.filter(option_field__icontains=field).values()
  print(form_options[0])
  return form_options[0]


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
    email = forms.EmailField(max_length=200, widget=forms.EmailInput, required=True)
    password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=True)

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

# Split into individual forms that display on the same page to look like different form sections.
class UserAdminUpdateForm(forms.Form):
  first_name = forms.CharField(max_length=200, widget=forms.TextInput, required=True)
  middle_name = forms.CharField(max_length=200, widget=forms.TextInput, required=False)  
  last_name = forms.CharField(max_length=200, widget=forms.TextInput, required=True)
  initials = forms.CharField(max_length=200, widget=forms.TextInput, required=False)
  nickname = forms.CharField(max_length=200, widget=forms.TextInput, required=False)
  email = forms.EmailField(max_length=200, widget=forms.EmailInput, required=True)
  phone = forms.CharField(max_length=200, widget=forms.TextInput, required=True)
  phone_type = forms.ChoiceField(widget=forms.Select, choices=PHONE_TYPE, required=False)
  apt_num = forms.CharField(max_length=10, widget=forms.TextInput, required=False)
  address = forms.CharField(max_length=150, widget=forms.TextInput, required=False)
  address_line2 = forms.CharField(max_length=150, widget=forms.TextInput, required=False)
  city = forms.CharField(max_length=35, widget=forms.TextInput, required=False)
  state = forms.ChoiceField(widget=forms.Select, choices=STATE_SELECT, required=False)
  zipcode = forms.IntegerField(widget=forms.TextInput, required=False)
  # occupation = forms.ChoiceField(widget=forms.Select, required=False)

  def __init__(self, *args, **kwargs):
    super(UserAdminUpdateForm, self).__init__(*args, **kwargs)
    self.fields = set_attributes(self.fields)
    # self.fields['occupation'] = forms.ChoiceField(choices=option_fields("occupation_type"))
    self.initial['Phone Type'] = 'Mobile'   
    

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
  return fields