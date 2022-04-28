from django import forms
from .models import Customer
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['location', 'avatar']
        # widgets = {
        #     'birthdate': DateInput(attrs={'type': 'date'}),
        # }