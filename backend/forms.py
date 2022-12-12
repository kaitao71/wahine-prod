from django import forms
from backend.models import *
from django.db import models
from django.contrib.auth.forms import UserCreationForm
# from dal import autocomplete
from django.contrib.auth import get_user_model
GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to respond', 'Prefer not to respond'),
    ]
class SignUpForm(UserCreationForm):

    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    class Meta:
        model = User
        fields = [
            "last_name",
            "email",
            "gender",
            "age",
            "referral_code",
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
    account_no = forms.CharField()
    account_value = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class EpfSocsoForm(forms.Form):
    is_epf_member = forms.CharField(required = False)
    is_socso_member = forms.CharField(required = False)
    epf_member_no = forms.CharField()
    socso_member_no = forms.CharField()
    epf_nominee_name = forms.CharField(required = False)
    socso_nominee_name = forms.CharField(required = False)
    epf_account_value = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class InsuranceForm(forms.Form):
    insurance_type = forms.CharField()
    provider_name = forms.CharField()
    policy_no = forms.CharField()
    nominee_name = forms.CharField(required = False)
    sum_insured = forms.CharField(required = False)
    insurance_type_2 = forms.CharField(required=False)
    provider_name_2 = forms.CharField(required=False)
    policy_no_2 = forms.CharField(required=False)
    nominee_name_2 = forms.CharField(required = False)
    sum_insured_2 = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

#Pending
class InvestmentForm(forms.Form):
    investment_type = forms.CharField()
    account_no = forms.CharField()
    fund_name = forms.CharField(required = False)
    account_value = forms.CharField(required = False)
    investment_type_2 = forms.CharField(required = False)
    account_no_2 = forms.CharField(required = False)
    fund_name_2 = forms.CharField(required = False)
    account_value_2 = forms.CharField(required = False)
    investment_type_3 = forms.CharField(required = False)
    account_no_3 = forms.CharField(required = False)
    fund_name_3 = forms.CharField(required = False)
    account_value_3 = forms.CharField(required = False)
    yesno = forms.CharField(required = False)


class PropertyForm(forms.Form):
    property_type = forms.CharField(required = False)
    residential_type = forms.CharField(required = False)
    address = forms.CharField()
    property_type_2 = forms.CharField(required = False)
    residential_type_2 = forms.CharField(required = False)
    address_2 = forms.CharField(required = False)
    ## Removed spa_price field  5/12/2022
    yesno = forms.CharField(required = False)

class VehicleForm(forms.Form):
    vehicle_type = forms.CharField(required = False)
    make_model = forms.CharField()
    registration_no = forms.CharField()
    vehicle_type_2 = forms.CharField(required = False)
    make_model_2 = forms.CharField(required = False)
    registration_no_2 = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class AssetOthersForm(forms.Form):
    asset_name = forms.CharField(required = False)
    asset_value = forms.CharField(required = False)
    asset_name_2 = forms.CharField(required = False)
    asset_value_2 = forms.CharField(required = False)
    asset_name_3 = forms.CharField(required = False)
    asset_value_3 = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class CreditCardForm(forms.Form):
    bank_name = forms.CharField()
    account_no = forms.CharField()
    amount_outstanding = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class PersonalLoanForm(forms.Form):
    bank_name = forms.CharField()
    account_no = forms.CharField()
    loan_amount = forms.CharField()
    loan_tenure = forms.CharField()
    loan_interest = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class PropertyLoanForm(forms.Form):
    bank_name = forms.CharField()
    account_no = forms.CharField()
    loan_amount = forms.CharField()
    loan_tenure = forms.CharField()
    loan_interest = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class VehicleLoanForm(forms.Form):
    bank_name = forms.CharField()
    account_no = forms.CharField()
    loan_amount = forms.CharField()
    loan_tenure = forms.CharField()
    loan_interest = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class LiabilitiesOthersForm(forms.Form):
    liability_name = forms.CharField(required = False)
    liability_value = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class NotifierForm(forms.Form):
    notifier_name = forms.CharField(required = False)
    notifier_email = forms.CharField(required = False)
    notifier_ic = forms.CharField(required = False)
    notifier_contactno = forms.CharField(required = False)
    notifier_relationship = forms.CharField(required = False)
    notifier_event = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class AccessListForm(forms.Form):
    accesslist_name = forms.CharField(required = False)
    accesslist_email = forms.CharField(required = False)
    accesslist_ic = forms.CharField(required = False)
    accesslist_contactno = forms.CharField(required = False)
    accesslist_relationship = forms.CharField(required = False)
    yesno = forms.CharField(required = False)
