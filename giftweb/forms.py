

#forms.py

from django import forms
from .models import *

from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import CryptoPayment



class PaymentForm(forms.ModelForm):
    gift_card_type = forms.ChoiceField(choices=[('apple', 'Apple Card'), ('amazon', 'Amazon Card'), ('steam', 'Steam Card'), ('xbox', 'Xbox Card')])

    code = forms.CharField(
        label='username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the Gift Card Code',
                'required': True,
            }
        )
    )
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    full_name = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Full Name',
                'required': True,
            }
        )
    )
    street_address = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Street Address',
                'required': True,
            }
        )
    )
    apartment_address = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Apartment Address',
                'required': True,
            }
        )
    )
    phone_number = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Phone No',
                'required': True,
            }
        )
    )
    quantity = forms.IntegerField(
        label='Quantity',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1',
                'required': True,
            }
        )
    )

    class Meta:
        model = Payment
        fields = ['quantity', 'amount', 'proof_of_pay', 'gift_card_type', 'code', 'country', 'full_name', 'street_address', 'apartment_address', 'phone_number']


#forms.py

class CryptoPaymentForm(forms.ModelForm):



    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    full_name = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Full Name',
                'required': True,
            }
        )
    )
    street_address = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Street Address',
                'required': True,
            }
        )
    )
    apartment_address = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Apartment Address',
                'required': True,
            }
        )
    )
    phone_number = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Phone No',
                'required': True,
            }
        )
    )
    quantity = forms.IntegerField(
        label='Quantity',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1',
                'required': True,
            }
        )
    )
    class Meta:
        model = Payment


    class Meta:
        model = CryptoPayment
        fields = ['quantity','payment_method', 'amount', 'proof_of_pay', 'country', 'full_name', 'street_address', 'apartment_address', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the amount field read-only
        self.fields['proof_of_pay'].widget.attrs['accept'] = 'image/*'
        

