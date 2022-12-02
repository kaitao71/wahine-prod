from django import forms
from backend.models import *
from django.db import models
from django.contrib.auth.forms import UserCreationForm
# from dal import autocomplete
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "last_name",
            "email",
            "password1",
        ]

class SubscriptionForm(forms.Form):
    plan = forms.CharField(required = True)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "mobile_number",
            "date_of_birth",
            "address",
            "city",
            "state",
            "postcode",
            "country",
            "gender",
            "marital",
        ]


class EnquiryForm(forms.Form):
    customer_email = models.EmailField()

BANK_TYPE_CHOICES = [
    ('Savings', 'Savings'),
    ('Credit Card', 'Credit Card'),
    ('Fixed Deposit','Fixed Deposit'),
]

# BANK_NAME_CHOICES = [
#     ('Affin Bank','Affin Bank'),
#     ('Alliance Bank','Alliance Bank'),
#     ('AmBank','AmBank'),
#     ('CIMB','CIMB'),
#     ('Hong Leong Bank','Hong Leong Bank'),
#     ('Maybank','Maybank'),
#     ('Public Bank','Public Bank'),
#     ('RHB Bank','RHB Bank'),
# ]

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
## Change bank type to account type
## add account value for bank, EPF
## insurance, add sum insured, remove other selection

## Investment - public/private
## unit trust means private investment ,change unit trust name to unit trust company management name

## property details - delete others

##move all blue colored fields to dashboard, instead of sign up flow

#vehicle - loan tenure instead of coverage
class BankAccountForm(forms.Form):
    account_type = forms.CharField()
    bank_name = forms.CharField()
    account_no = forms.CharField(required = False)
    account_value = forms.CharField(required = False)

class EpfSocsoForm(forms.Form):
    is_epf_member = forms.CharField()
    is_socso_member = forms.CharField()
    epf_member_no = forms.CharField(required = False)
    socso_member_no = forms.CharField(required = False)
    epf_nominee_name = forms.CharField(required = False)
    socso_nominee_name = forms.CharField(required = False)
    epf_account_value = forms.CharField(required = False)
    socso_account_value = forms.CharField(required = False)

class InsuranceForm(forms.Form):
    insurance_type = forms.CharField(required = False)
    policy_no = forms.CharField(required = False)
    nominee_name = forms.CharField(required = False)
    account_value = forms.CharField(required = False)

class InvestmentForm(forms.Form):
    investment_type = forms.CharField(required = False)
    account_no = forms.CharField(required = False)
    fund_name = forms.CharField(required = False)
    account_value = forms.CharField(required = False)

class PropertyForm(forms.Form):
    property_type = forms.CharField(required = False)
    residential_type = forms.CharField(required = False)
    address = forms.CharField(required = False)
    spa_price = forms.CharField(required = False)

class VehicleForm(forms.Form):
    vehicle_type = forms.CharField(required = False)
    make_model = forms.CharField(required = False)
    registration_no = forms.CharField(required = False)

class AssetOthersForm(forms.Form):
    asset_name = forms.CharField(required = False)
    asset_value = forms.CharField(required = False)

class CreditCardForm(forms.Form):
    bnpl_service = forms.CharField(required = False)
    bank_name = forms.CharField(required = False)
    account_no = forms.CharField(required = False)
    amount_outstanding = forms.CharField(required = False)

class PersonalLoanForm(forms.Form):
    bank_name = forms.CharField(required = False)
    account_no = forms.CharField(required = False)
    loan_amount = forms.CharField(required = False)
    loan_tenure = forms.CharField(required = False)
    loan_interest = forms.CharField(required = False)

class PropertyLoanForm(forms.Form):
    bank_name = forms.CharField(required = False)
    account_no = forms.CharField(required = False)
    loan_amount = forms.CharField(required = False)
    loan_tenure = forms.CharField(required = False)
    loan_interest = forms.CharField(required = False)

class VehicleLoanForm(forms.Form):
    bank_name = forms.CharField(required = False)
    account_no = forms.CharField(required = False)
    loan_amount = forms.CharField(required = False)
    loan_tenure = forms.CharField(required = False)
    loan_interest = forms.CharField(required = False)

class LiabilitiesOthersForm(forms.Form):
    bank_name = forms.CharField(required = False)
    account_no = forms.CharField(required = False)
    loan_amount = forms.CharField(required = False)
    loan_tenure = forms.CharField(required = False)
    loan_interest = forms.CharField(required = False)
