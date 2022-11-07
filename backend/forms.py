from django import forms
from backend.models import *
from django.db import models
from django.contrib.auth.forms import UserCreationForm
# from dal import autocomplete
from django.contrib.auth import get_user_model


class EnquiryForm(forms.Form):
    customer_email = models.EmailField()

BANK_TYPE_CHOICES = [
    ('Savings', 'Savings'),
    ('Credit Card', 'Credit Card'),
    ('Fixed Deposit','Fixed Deposit'),
    ('Other','Other'),
]

BANK_NAME_CHOICES = [
    ('Affin Bank','Affin Bank'),
    ('Alliance Bank','Alliance Bank'),
    ('AmBank','AmBank'),
    ('CIMB','CIMB'),
    ('Hong Leong Bank','Hong Leong Bank'),
    ('Maybank','Maybank'),
    ('Public Bank','Public Bank'),
    ('RHB Bank','RHB Bank'),
]

INSURANCE_CHOICES = [
('Life','Life'),
('General','General'),
('Medical','Medical'),
('Others','Others'),
]
BOOLEAN_CHOICES = [
    ('Yes','Yes'),
    ('No','No'),
    ]

class BankAccountForm(forms.Form):
    bank_type = forms.ChoiceField(choices = BANK_TYPE_CHOICES,widget=forms.RadioSelect())
    bank_name = forms.ChoiceField(choices = BANK_NAME_CHOICES)
    account_no = forms.CharField(required = False)

class BankAccountForm2(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('user','data','item_type',)

class EpfSocsoForm(forms.Form):
    is_epf_member = forms.ChoiceField(choices = BOOLEAN_CHOICES,widget=forms.RadioSelect())
    is_socso_member = forms.ChoiceField(choices = BOOLEAN_CHOICES,widget=forms.RadioSelect())
    epf_member_no = forms.CharField(required = True)
    socso_member_no = forms.CharField(required = False)
    epf_nominee_name = forms.CharField(required = False)
    socso_nominee_name = forms.CharField(required = False)

class EpfForm(forms.Form):
    is_member = forms.ChoiceField(choices = BOOLEAN_CHOICES,widget=forms.RadioSelect())
    member_no = forms.CharField(required = False)
    nominee_name = forms.CharField(required = False)

class SocsoForm(forms.Form):
    is_member = forms.ChoiceField(choices = BOOLEAN_CHOICES,widget=forms.RadioSelect())
    member_no = forms.CharField(required = False)
    nominee_name = forms.CharField(required = False)

class InsuranceForm(forms.Form):
    insurance_type = forms.ChoiceField(choices = INSURANCE_CHOICES,widget=forms.RadioSelect())
    policy_no = forms.CharField(required = False)
    nominee_name = forms.CharField(required = False)
