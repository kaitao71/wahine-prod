from django import forms
from backend.models import *
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory, inlineformset_factory
# from dal import autocomplete
from django.contrib.auth import get_user_model
GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to respond', 'Prefer not to respond'),
    ]

class EpfForm(forms.ModelForm):
    class Meta:
        model = Epf
        fields = ['account_no','account_value','nominee_name',]

class SocsoForm(forms.ModelForm):
    class Meta:
        model = Socso
        fields = ['account_no','nominee_name',]

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['account_type','bank_name','account_no','account_value',]

ACCOUNT_TYPE_CHOICES = [
        ('Saving Account', 'Saving Account'),
        ('Current Account', 'Current Account'),
        ('Fixed Deposit', 'Fixed Deposit'),
    ]

BankModelFormset = modelformset_factory(
    Bank,
    fields=('account_type',
            'bank_name',
            'account_no',
            'account_value',
            ),
    extra=1,
    widgets={'account_type': forms.RadioSelect(choices=ACCOUNT_TYPE_CHOICES,attrs={
        }),
            'bank_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter bank name here'
        }
        )
    }
)

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = ['provider','policy_no','nominee_name','sum_insured',]

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['account_type','bank_name','account_no','account_value',]

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['account_type','bank_name','account_no','account_value',]

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['account_type','bank_name','account_no','account_value',]

class OtherAssetForm(forms.ModelForm):
    class Meta:
        model = OtherAsset
        fields = ['name','value',]
        
class EditItemModelForm(forms.ModelForm):

    def __init__(self, *args, instance=None, **kwargs):
        super(EditItemModelForm, self).__init__(*args, instance=instance, **kwargs)
        if instance:
            self.fields['item_type'] = forms.CharField()

    def save(self, commit=True):
        self.fields['insurance_type'] = self.cleaned_data.get(f'insurance_type', '')
        self.fields['item_type'] = ""
        return super(InsuranceModelForm, self).save(commit=commit)

    class Meta:
        model = Item
        fields = ['item_type',]

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

EVENT_CHOICES =(
    ("Critical Illness", "Critical Illness"),
    ("Death", "Death"),
    ("Dementia", "Dementia"),
    ("Permanent Disability", "Permanent Disability"),
)


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
class EditItemModelForm(forms.ModelForm):

    def __init__(self, *args, instance=None, **kwargs):
        super(EditItemModelForm, self).__init__(*args, instance=instance, **kwargs)
        if instance:
            self.fields['item_type'] = forms.CharField()

    def save(self, commit=True):
        # self.fields['insurance_type'] = self.cleaned_data.get(f'insurance_type', '')
        self.fields['item_type'] = ""
        return super(InsuranceModelForm, self).save(commit=commit)

    class Meta:
        model = Item
        fields = ['item_type']

class BankAccountForm(forms.Form):
    account_type = forms.CharField()
    bank_name = forms.CharField()
    account_no = forms.CharField()
    account_type_2 = forms.CharField(required=False)
    bank_name_2 = forms.CharField(required=False)
    account_no_2 = forms.CharField(required=False)
    account_value_2 = forms.CharField(required=False)
    account_value = forms.IntegerField(required = False)
    yesno = forms.CharField(required = False)

class EpfSocsoForm(forms.Form):
    is_epf_member = forms.CharField(required = False)
    is_socso_member = forms.CharField(required = False)
    epf_member_no = forms.CharField()
    socso_member_no = forms.CharField()
    epf_nominee_name = forms.CharField(required = False)
    socso_nominee_name = forms.CharField(required = False)
    epf_account_value = forms.IntegerField(required = False)
    yesno = forms.CharField(required = False)

class InsuranceForm(forms.Form):
    insurance_type = forms.CharField()
    provider_name = forms.CharField()
    provider_name_custom = forms.CharField(required = False)
    policy_no = forms.CharField()
    nominee_name = forms.CharField(required = False)
    sum_insured = forms.IntegerField(required = False)
    insurance_type_2 = forms.CharField(required=False)
    provider_name_2 = forms.CharField(required=False)
    provider_name_custom_2 = forms.CharField(required=False)
    policy_no_2 = forms.CharField(required=False)
    nominee_name_2 = forms.CharField(required = False)
    sum_insured_2 = forms.IntegerField(required = False)
    yesno = forms.CharField(required = False)

#Pending
class InvestmentForm(forms.Form):
    investment_type = forms.CharField()
    account_no = forms.CharField()
    fund_name = forms.CharField(required = False)
    account_value = forms.IntegerField(required = False)
    investment_type_2 = forms.CharField(required = False)
    account_no_2 = forms.CharField(required = False)
    fund_name_2 = forms.CharField(required = False)
    account_value_2 = forms.IntegerField(required = False)
    investment_type_3 = forms.CharField(required = False)
    account_no_3 = forms.CharField(required = False)
    fund_name_3 = forms.CharField(required = False)
    account_value_3 = forms.IntegerField(required = False)
    yesno = forms.CharField(required = False)


class PropertyForm(forms.Form):
    property_type = forms.CharField(required = False)
    residential_type = forms.CharField(required = False)
    address = forms.CharField()
    state = forms.CharField(required = False)
    postcode = forms.CharField(required = False)
    titleno = forms.CharField(required = False) 
    property_type_2 = forms.CharField(required = False)
    residential_type_2 = forms.CharField(required = False)
    address_2 = forms.CharField(required = False)
    state_2= forms.CharField(required = False)
    postcode_2 = forms.CharField(required = False)
    titleno_2 = forms.CharField(required = False)
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
    bank_name_2 = forms.CharField(required = False)
    account_no_2 = forms.CharField(required = False)
    amount_outstanding_2 = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class PersonalLoanForm(forms.Form):
    bank_name = forms.CharField()
    account_no = forms.CharField()
    loan_amount = forms.IntegerField()
    loan_tenure = forms.CharField()
    bank_name_2 = forms.CharField(required=False)
    account_no_2 = forms.CharField(required=False)
    loan_amount_2 = forms.IntegerField(required=False)
    loan_tenure_2 = forms.CharField(required=False)
    loan_interest = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class PropertyLoanForm(forms.Form):
    bank_name = forms.CharField()
    account_no = forms.CharField()
    loan_amount = forms.IntegerField()
    loan_tenure = forms.CharField()
    bank_name_2 = forms.CharField(required=False)
    account_no_2 = forms.CharField(required=False)
    loan_amount_2 = forms.IntegerField(required=False)
    loan_tenure_2 = forms.CharField(required=False)
    yesno = forms.CharField(required = False)

class VehicleLoanForm(forms.Form):
    bank_name = forms.CharField()
    account_no = forms.CharField()
    loan_amount = forms.IntegerField()
    loan_tenure = forms.CharField()
    bank_name_2 = forms.CharField(required=False)
    account_no_2 = forms.CharField(required=False)
    loan_amount_2 = forms.IntegerField(required=False)
    loan_tenure_2 = forms.CharField(required=False)
    loan_interest = forms.CharField(required = False)
    yesno = forms.CharField(required = False)

class LiabilitiesOthersForm(forms.Form):
    liability_name = forms.CharField(required = False)
    liability_value = forms.IntegerField(required = False)
    liability_name_2 = forms.CharField(required = False)
    liability_value_2 = forms.IntegerField(required = False)
    liability_name_3 = forms.CharField(required = False)
    liability_value_3 = forms.IntegerField(required = False)
    yesno = forms.CharField(required = False)

class NotifierForm(forms.Form):
    notifier_name = forms.CharField()
    notifier_email = forms.CharField()
    notifier_ic = forms.CharField(required = False)
    notifier_contactno = forms.CharField(required = False)
    notifier_relationship = forms.CharField(required = False)
    notifier_event = forms.MultipleChoiceField(choices=EVENT_CHOICES,required = False)  
    notifier_name_2 = forms.CharField(required = False)
    notifier_email_2 = forms.CharField(required = False)
    notifier_ic_2 = forms.CharField(required = False)
    notifier_contactno_2 = forms.CharField(required = False)
    notifier_relationship_2 = forms.CharField(required = False)
    notifier_event_2 = forms.MultipleChoiceField(choices=EVENT_CHOICES,required = False)
    yesno = forms.CharField(required = False)

class AccessListForm(forms.Form):
    accesslist_name = forms.CharField()
    accesslist_email = forms.CharField()
    accesslist_ic = forms.CharField(required = False)
    accesslist_contactno = forms.CharField(required = False)
    accesslist_relationship = forms.CharField(required = False)
    accesslist_event = forms.MultipleChoiceField(choices=EVENT_CHOICES,required = False)  
    accesslist_name_2 = forms.CharField(required = False)
    accesslist_email_2 = forms.CharField(required = False)
    accesslist_ic_2 = forms.CharField(required = False)
    accesslist_contactno_2 = forms.CharField(required = False)
    accesslist_relationship_2 = forms.CharField(required = False)
    accessliost_event_2 = forms.MultipleChoiceField(choices=EVENT_CHOICES,required = False)  
    yesno = forms.CharField(required = False)
