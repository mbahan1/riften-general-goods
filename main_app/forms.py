from django import forms
from .models import Customer
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import UserCreationForm

# class UserForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['location', 'avatar']

PAYMENT = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '1234 Main St'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Apartment or suite'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT)