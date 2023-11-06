from .models import User
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
  check_pass = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=True)

  def __init__(self, *args, **kwargs):
    super(Register_Form, self).__init__(*args, **kwargs)
    for name in self.fields.keys():
      self.fields[name].widget.attrs.update({
        'class' : 'form-control',
      })
      self.fields['password'].widget.attrs.update({
        'id': 'password',
      })
      self.fields['check_pass'].widget.attrs.update({
        'class' : 'form-control',
        'id': 'check_pass',
        'onChange': 'checkPass();'
      })
      self.fields['password'].label = 'Password'
      self.fields['check_pass'].label = 'Password Confirmation'

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
        # check_pass = self.cleaned_data.get('check_pass')

class Login_Form(forms.Form): 
    login_email = forms.EmailField(max_length=200, widget=forms.EmailInput)
    login_password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(Login_Form, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })
            self.fields['login_password'].widget.attrs.update({
                'class' : 'form-control',
                'id' : 'login_password',
                '@change': 'passEnbl();',
                'v-model': 'password'
            })
            self.fields['login_password'].label = 'Password'

