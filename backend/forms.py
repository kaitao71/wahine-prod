from django import forms
from backend.models import *
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory, inlineformset_factory
# from dal import autocomplete
from django.contrib.auth import get_user_model

""" Beginning of V2 Forms """

ACCOUNT_TYPE_CHOICES = [
        ('Saving Account', 'Saving Account'),
        ('Current Account', 'Current Account'),
        ('Fixed Deposit', 'Fixed Deposit'),
    ]

BANK_NAME_CHOICES = [
        ('AEON Credit Service (M) Berhad','AEON Credit Service (M) Berhad'),
        ('Affin Bank Berhad','Affin Bank Berhad'),
        ('Affin Islamic Bank Berhad','Affin Islamic Bank Berhad'),
        ('Alliance Bank Malaysia Berhad','Alliance Bank Malaysia Berhad'),
        ('Al Rajhi Banking & Investment Corporation (Malaysia) Berhad','Al Rajhi Banking & Investment Corporation (Malaysia) Berhad'),
        ('AmBank (M) Berhad','AmBank (M) Berhad'),
        ('AmBank Islamic Berhad','AmBank Islamic Berhad'),
        ('Bank Islam Malaysia Berhad (BIMB)','Bank Islam Malaysia Berhad (BIMB)'),
        ('Bank Kerjasama Rakyat Malaysia Berhad (Bank Rakyat)','Bank Kerjasama Rakyat Malaysia Berhad (Bank Rakyat)'),
        ('Bank Muamalat Malaysia Berhad','Bank Muamalat Malaysia Berhad'),
        ('Bank of America Malaysia Berhad','Bank of America Malaysia Berhad'),
        ('Bank of China (Malaysia) Berhad','Bank of China (Malaysia) Berhad'),
        ('Bank Pertanian Malaysia Berhad (Agrobank)','Bank Pertanian Malaysia Berhad (Agrobank)'),
        ('Bank Simpanan Nasional','Bank Simpanan Nasional'),
        ('CIMB Bank Berhad','CIMB Bank Berhad'),
        ('CIMB Islamic Bank Berhad','CIMB Islamic Bank Berhad'),
        ('Citibank Berhad','Citibank Berhad'),
        ('Deutsche Bank (Malaysia) Berhad','Deutsche Bank (Malaysia) Berhad'),
        ('Hong Leong Bank Berhad','Hong Leong Bank Berhad'),
        ('HSBC Amanah Malaysia Berhad','HSBC Amanah Malaysia Berhad'),
        ('HSBC Bank Malaysia Berhad','HSBC Bank Malaysia Berhad'),
        ('Industrial and Commercial Bank of China (Malaysia) Berhad','Industrial and Commercial Bank of China (Malaysia) Berhad'),
        ('J.P. Morgan Chase Bank Berhad','J.P. Morgan Chase Bank Berhad'),
        ('Kuwait Finance House','Kuwait Finance House'),
        ('Malayan Banking Berhad','Malayan Banking Berhad'),
        ('Maybank Islamic Berhad','Maybank Islamic Berhad'),
        ('OCBC Bank (Malaysia) Berhad','OCBC Bank (Malaysia) Berhad'),
        ('Public Bank Berhad','Public Bank Berhad'),
        ('Public Islamic Bank Berhad','Public Islamic Bank Berhad'),
        ('RHB Bank Berhad','RHB Bank Berhad'),
        ('RHB Islamic Bank Berhad','RHB Islamic Bank Berhad'),
        ('Standard Chartered Bank Malaysia Berhad','Standard Chartered Bank Malaysia Berhad'),
        ('United Overseas Bank (Malaysia) Berhad','United Overseas Bank (Malaysia) Berhad'),
    ]

INSURANCE_PROVIDER_CHOICES = [
        ('AIA Berhad','AIA Berhad'),
        ('AIA General Berhad','AIA General Berhad'),
        ('AIA PUBLIC Takaful Berhad','AIA PUBLIC Takaful Berhad'),
        ('AIG Malaysia Insurance Berhad','AIG Malaysia Insurance Berhad'),
        ('Allianz General Insurance Company (Malaysia) Berhad','Allianz General Insurance Company (Malaysia) Berhad'),
        ('Allianz Life Insurance Malaysia Berhad','Allianz Life Insurance Malaysia Berhad'),
        ('AmGeneral Insurance Berhad','AmGeneral Insurance Berhad'),
        ('AmMetLife Insurance Berhad','AmMetLife Insurance Berhad'),
        ('AmMetLife Takaful Berhad','AmMetLife Takaful Berhad'),
        ('AXA Affin General Insurance Berhad','AXA Affin General Insurance Berhad'),
        ('AXA Affin Life Insurance Berhad','AXA Affin Life Insurance Berhad'),
        ('Berjaya Sompo Insurance Berhad','Berjaya Sompo Insurance Berhad'),
        ('Chubb Insurance Malaysia Berhad','Chubb Insurance Malaysia Berhad'),
        ('Danajamin Nasional Berhad','Danajamin Nasional Berhad'),
        ('Etiqa Family Takaful Berhad','Etiqa Family Takaful Berhad'),
        ('Etiqa General Insurance Berhad','Etiqa General Insurance Berhad'),
        ('Etiqa General Takaful Berhad','Etiqa General Takaful Berhad'),
        ('Etiqa Life Insurance Berhad','Etiqa Life Insurance Berhad'),
        ('FWD Takaful Berhad','FWD Takaful Berhad'),
        ('Gibraltar BSN Life Berhad','Gibraltar BSN Life Berhad'),
        ('Great Eastern General Insurance (Malaysia) Berhad','Great Eastern General Insurance (Malaysia) Berhad'),
        ('Eastern General Insurance (Malaysia) Berhad','Eastern General Insurance (Malaysia) Berhad'),
        ('Great Eastern Life Assurance (Malaysia) Berhad','Great Eastern Life Assurance (Malaysia) Berhad'),
        ('Great Eastern Takaful Berhad','Great Eastern Takaful Berhad'),
        ('Hong Leong Assurance Berhad','Hong Leong Assurance Berhad'),
        ('Hong Leong MSIG Takaful Berhad','Hong Leong MSIG Takaful Berhad'),
        ('Liberty Insurance Berhad','Liberty Insurance Berhad'),
        ('Lonpac Insurance Berhad','Lonpac Insurance Berhad'),
        ('Manulife Insurance Berhad','Manulife Insurance Berhad'),
        ('MCIS Insurance Berhad','MCIS Insurance Berhad'),
        ('MPI Generali Insurans Berhad','MPI Generali Insurans Berhad'),
        ('MSIG Insurance (Malaysia) Bhd','MSIG Insurance (Malaysia) Bhd'),
        ('Pacific & Orient Insurance Co. Berhad','Pacific & Orient Insurance Co. Berhad'),
        ('Pacific Insurance Berhad','Pacific Insurance Berhad'),
        ('Progressive Insurance Berhad','Progressive Insurance Berhad'),
        ('Prudential Assurance Malaysia Berhad','Prudential Assurance Malaysia Berhad'),
        ('Prudential BSN Takaful Berhad','Prudential BSN Takaful Berhad'),
        ('QBE Insurance (Malaysia) Berhad','QBE Insurance (Malaysia) Berhad'),
        ('RHB Insurance Berhad','RHB Insurance Berhad'),
        ('Sun Life Malaysia Assurance Berhad','Sun Life Malaysia Assurance Berhad'),
        ('Syarikat Takaful Malaysia Am Berhad','Syarikat Takaful Malaysia Am Berhad'),
        ('Syarikat Takaful Malaysia Keluarga Berhad','Syarikat Takaful Malaysia Keluarga Berhad'),
        ('Takaful Ikhlas Family Berhad','Takaful Ikhlas Family Berhad'),
        ('Takaful Ikhlas General Berhad','Takaful Ikhlas General Berhad'),
        ('Tokio Marine Insurance (Malaysia) Berhad','Tokio Marine Insurance (Malaysia) Berhad'),
        ('Tokio Marine Life Insurance Malaysia Bhd','Tokio Marine Life Insurance Malaysia Bhd'),
        ('Tune Insurance Malaysia Berhad','Tune Insurance Malaysia Berhad'),
        ('Zurich General Insurance Malaysia Berhad','Zurich General Insurance Malaysia Berhad'),
        ('Zurich General Takaful Malaysia Berhad','Zurich General Takaful Malaysia Berhad'),
        ('Zurich Life Insurance Malaysia Berhad','Zurich Life Insurance Malaysia Berhad'),
        ('Zurich Takaful Malaysia Berhad','Zurich Takaful Malaysia Berhad'),
    ]

RESIDENTIAL_TYPE_CHOICES = [
        ('Landed','Landed'),
        ('Condominium','Condominium'),
        ('Shop Lot','Shop Lot'),
        ('Factory','Factory'),
        ('Residential','Residential'),
        ('Commercial','Commercial'),
    ]

INSURANCE_TYPE_CHOICES = [
        ('Life', 'Life'),
        ('Medical', 'Medical'),
        ('General', 'General'),
    ]


GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to respond', 'Prefer not to respond'),
    ]

BankModelFormset = modelformset_factory(
    Bank,
    fields=('account_type',
            'bank_name',
            'account_no',
            'account_value',
            'user',
            ),
    extra=1,
    widgets={
        'account_type': forms.RadioSelect(choices=ACCOUNT_TYPE_CHOICES,attrs={
        }),
        'bank_name': forms.Select(choices=BANK_NAME_CHOICES,attrs={
            'class': 'form-control',
            'placeholder': 'Select a bank'
        }),
        'account_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account no. here'
        }),
        'account_value': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account value here'
        })
    ,
    }
)

InsuranceModelFormset = modelformset_factory(
    Insurance,
    fields=('insurance_type',
            'provider',
            'policy_no',
            'nominee_name',
            'sum_insured',
            'user',
            ),
    extra=1,
    widgets={
        'insurance_type': forms.RadioSelect(choices=INSURANCE_TYPE_CHOICES,attrs={
        }),
        'provider': forms.Select(choices=INSURANCE_PROVIDER_CHOICES,attrs={
            'class': 'form-control',
            'placeholder': 'Select a provider'
        }),
        'policy_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter policy no. here'
        }),
        'nominee_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter nominee name here'
        }),
        'sum_insured': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter sum insured here'
        }),
    }
)

# InvestmentModelFormset = modelformset_factory(
#     Investment,
#     fields=('insurance_type',
#             'provider',
#             'policy_no',
#             'nominee_name',
#             'sum_insured',
#             ),
#     extra=1,
#     widgets={
#         'insurance_type': forms.RadioSelect(choices=INSURANCE_TYPE_CHOICES,attrs={
#         }),
#         'provider': forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter provider name here'
#         }),
#         'policy_no': forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter policy no. here'
#         }),
#         'nominee_name': forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter nominee name here'
#         }),
#         'sum_insured': forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter sum insured here'
#         }),
#     }
# )

PROPERTY_TYPE_CHOICES = [
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
        ('Land', 'Land'),
    ]

PropertyModelFormset = modelformset_factory(
    Property,
    fields=('property_type',
            'residential_type',
            'address',
            'state',
            'postcode',
            'titleno',
            'user',
            ),
    extra=1,
    widgets={
        'property_type': forms.RadioSelect(choices=PROPERTY_TYPE_CHOICES,attrs={
        }),
        'residential_type': forms.Select(choices=RESIDENTIAL_TYPE_CHOICES,attrs={
            'class': 'form-control',
            'placeholder': 'Enter residential type here'
        }),
        'address': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter address here'
        }),
        'state': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter state here'
        }),
        'postcode': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter postcode here'
        }),
        'titleno': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter title no here'
        }),
    }
)

VEHICLE_TYPE_CHOICES = [
        ('Car', 'Car'),
        ('Motocycle', 'Motocycle'),
    ]

VehicleModelFormset = modelformset_factory(
    Vehicle,
    fields=('vehicle_type',
            'registration_no',
            'make_model',
            'user',
            ),
    extra=1,
    widgets={
        'vehicle_type': forms.Select(choices=VEHICLE_TYPE_CHOICES,attrs={
            'class': 'form-control',
            'placeholder': 'Select a vehicle type',
        }),
        'registration_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter registration no here'
        }),
        'make_model': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter make model here'
        }),
    }
)


OtherAssetModelFormset = modelformset_factory(
    OtherAsset,
    fields=('name',
            'value',
            'user',
            ),
    extra=1,
    widgets={
        'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter asset name here'
        }),
        'value': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter asset value here'
        }),
    }
)

class EpfForm(forms.ModelForm):
    class Meta:
        model = Epf
        fields = ['account_no','account_value','nominee_name','user']
        widgets={
            'account_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account value here'
        }),
            'account_value': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account value here'
        }),
            'nominee_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter nominee name here'
        }),
        }

class SocsoForm(forms.ModelForm):
    class Meta:
        model = Socso
        fields = ['account_no','nominee_name','user']
        widgets={
            'account_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account value here'
        }),
            'nominee_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter nominee name here'
        }),
        }


CreditCardModelFormset = modelformset_factory(
    CreditCard,
    fields=(
            'bank_name',
            'account_no',
            'amount_outstanding',
            'user',
            ),
    extra=1,
    widgets={
        'bank_name': forms.RadioSelect(choices=BANK_NAME_CHOICES,attrs={
        }),
        'account_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account no. here'
        }),
        'amount_outstanding': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount outstanding here'
        }),
    }
)

PersonalLoanModelFormset = modelformset_factory(
    PersonalLoan,
    fields=(
            'bank_name',
            'account_no',
            'amount_outstanding',
            'user',
            ),
    extra=1,
    widgets={
        'bank_name': forms.RadioSelect(choices=BANK_NAME_CHOICES,attrs={
        }),
        'account_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account no. here'
        }),
        'amount_outstanding': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount outstanding here'
        }),
        'loan_tenure': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter loan tenure here'
        }),
    }
)

VehicleLoanModelFormset = modelformset_factory(
    VehicleLoan,
    fields=(
            'bank_name',
            'account_no',
            'amount_outstanding',
            'user',
            ),
    extra=1,
    widgets={
        'bank_name': forms.RadioSelect(choices=BANK_NAME_CHOICES,attrs={
        }),
        'account_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account no. here'
        }),
        'amount_outstanding': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount outstanding here'
        }),
        'loan_tenure': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter loan tenure here'
        }),
    }
)

PropertyLoanModelFormset = modelformset_factory(
    PropertyLoan,
    fields=(
            'bank_name',
            'account_no',
            'amount_outstanding',
            'user',
            ),
    extra=1,
    widgets={
        'bank_name': forms.RadioSelect(choices=BANK_NAME_CHOICES,attrs={
        }),
        'account_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account no. here'
        }),
        'amount_outstanding': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount outstanding here'
        }),
        'loan_tenure': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter loan tenure here'
        }),
    }
)

OtherLiabilityModelFormset = modelformset_factory(
    OtherLiability,
    fields=('name',
            'value',
            'user',
            ),
    extra=1,
    widgets={
        'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter liability name here'
        }),
        'value': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter liability value here'
        }),
    }
)
""" End of V2 Forms """  


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['account_type','bank_name','account_no','account_value',]

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = ['provider','policy_no','nominee_name','sum_insured',]

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['account_type','bank_name','account_no','account_value',]

# class PropertyForm(forms.ModelForm):
#     class Meta:
#         model = Property
#         fields = ['account_type','bank_name','account_no','account_value',]

# class VehicleForm(forms.ModelForm):
#     class Meta:
#         model = Vehicle
#         fields = ['account_type','bank_name','account_no','account_value',]

# class OtherAssetForm(forms.ModelForm):
#     class Meta:
#         model = OtherAsset
#         fields = ['name','value',]

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
    account_no = forms.CharField(required = False)
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
