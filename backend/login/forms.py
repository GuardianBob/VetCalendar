from .models import User, UserPass, Address, CityState, Phone, AccessLevel, UserPrivileges, Occupation, FormOptions
from django import forms
import datetime
import bcrypt


STATE_SELECT = (
    ('', 'Select State'),
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
    "occupation": "Occupation",
    "old_password": "Old Password",
    "new_password": "New Password",
    "verify_password": "Verify Password",
}

# PHONE_TYPE = (
#   ('mobile', 'Mobile'),
#   ('home', 'Home'),
#   ('work', 'Work'),
#   ('other', 'Other')
# )

# USER_OCCUPATION = (
#   ('doctor', 'Doctor'),
#   ('tech', 'Technician'),
#   ('other', 'Other')
# )

def option_fields(field):
  form_options = FormOptions.objects.filter(option_field__icontains=field)
  print(form_options.values())
  return form_options

def field_options(field):
  form_options = FormOptions.objects.filter(option_model=field)
  print(form_options.values())
  return form_options


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

  # def clean(self):
  #   super(Register_Form, self).clean()
  #   first_name = self.cleaned_data.get('first_name')
  #   last_name = self.cleaned_data.get('last_name')
  #   email = self.cleaned_data.get('email')
  #   address = self.cleaned_data.get('address')
  #   address_line2 = self.cleaned_data.get('address_line2')
  #   apt_num = self.cleaned_data.get('apt_num')
  #   city = self.cleaned_data.get('city')
  #   state = self.cleaned_data.get('state')
  #   zipcode = self.cleaned_data.get('zipcode')
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
  phone_type = forms.ChoiceField(widget=forms.Select, required=False)

  def __init__(self, *args, **kwargs):
    super(UserCreationForm, self).__init__(*args, **kwargs)
    self.fields = set_attributes(self.fields)
    self = identify_choice_fields(self)
    # self.initial['phone_type'] = 'mobile'

# Split into individual forms that display on the same page to look like different form sections.
class UserAdminUpdateForm(forms.Form):
  first_name = forms.CharField(max_length=200, widget=forms.TextInput, required=True)
  middle_name = forms.CharField(max_length=200, widget=forms.TextInput, required=False)  
  last_name = forms.CharField(max_length=200, widget=forms.TextInput, required=True)
  initials = forms.CharField(max_length=200, widget=forms.TextInput, required=False)
  nickname = forms.CharField(max_length=200, widget=forms.TextInput, required=False)
  email = forms.EmailField(max_length=200, widget=forms.EmailInput, required=True)
  phone = forms.CharField(max_length=200, widget=forms.TextInput, required=False)
  phone_type = forms.ChoiceField(widget=forms.Select, required=False)
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
    # options = option_fields('phone_type')
    # self.fields['phone_type'].choices = [(option.option, option.option_label) for option in options]
    self = identify_choice_fields(self)
    # self.initial['phone_type'] = 'mobile'
    # for field_name, field in self.fields.items():
    #   if isinstance(field, forms.ChoiceField):
    #     f_options = option_fields(field_name) 
    #     if f_options:
    #       self.fields[field_name].choices = [(option.option, option.option_label) for option in f_options]
    #     print(f"{field_name} is a ChoiceField")
    # self.fields['occupation'] = forms.ChoiceField(choices=option_fields("occupation_type"))

class UpdatePasswordForm(forms.Form):
  old_password = forms.CharField(max_length=50, min_length=8, widget=forms.PasswordInput, required=True)
  new_password = forms.CharField(max_length=50, min_length=8, widget=forms.PasswordInput, required=True)
  verify_password = forms.CharField(max_length=50, min_length=8, widget=forms.PasswordInput, required=True)

  def __init__(self, *args, **kwargs):
    super(UpdatePasswordForm, self).__init__(*args, **kwargs)
    self.fields = set_attributes(self.fields)

class UpdateOccupationForm(forms.ModelForm):
  # Create form from Occupation model
  class Meta:
    model = Occupation
    fields = ['occupation']
  # occupation = forms.ChoiceField(widget=forms.Select, required=False)

  def __init__(self, *args, **kwargs):
    if args:
      # Extract the first value from the queryset if it's not None
      args = (args[0].values().first(),) if args[0] else args
    super(UpdateOccupationForm, self).__init__(*args, **kwargs)
    self.fields['occupation'] = forms.ChoiceField(widget=forms.Select, required=False)
    self = identify_choice_fields(self)
    # options = field_options('occupation')
    # self.fields['occupation'].choices = [(option.option, option.option_label) for option in options]
    self.fields = set_attributes(self.fields)

  def from_user(user):
      return UpdateOccupationForm(user.user_occupation.values().first())

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

def identify_choice_fields(form):
  for field_name, field in form.fields.items():
    if isinstance(field, forms.ChoiceField):
      print(f"{field_name} is a ChoiceField")
      f_options = option_fields(field_name) 
      if f_options:
        if field_name == 'phone_type':
          form.fields['phone_type'].choices = [('', 'Phone Type')] + [(option.option, option.option_label) for option in f_options]
        else:
          form.fields[field_name].choices = [('', '')] + [(option.option, option.option_label) for option in f_options]
  return form