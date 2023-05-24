from django import forms
from backend.models import *
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory, inlineformset_factory
# from dal import autocomplete
from django.contrib.auth import get_user_model
import re
""" Beginning of V2 Forms """
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django_registration.forms import RegistrationForm

from backend.models import *


class MyCustomUserForm(RegistrationForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, initial='Female')
    class Meta(RegistrationForm.Meta):
        model = User
        fields = [
            "last_name",
            "email",
            "gender",
            "age",
            "referral_code",
            "password1",
        ]


ACCOUNT_TYPE_CHOICES = [
        ('Saving Account', 'Savings Account'),
        ('Current Account', 'Current Account'),
        ('Fixed Deposit', 'Fixed Deposit'),
    ]

OVERSEAS_OR_LOCAL = [
        ('Local', 'Local'),
        ('Oversea', 'Oversea'),
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

UNIT_TRUST_CHOICES = [
('Abrdn Islamic Malaysia Sdn Bhd','Abrdn Islamic Malaysia Sdn Bhd'),
('Affin Bank Berhad','Affin Bank Berhad'),
('Affin Islamic Bank Berhad','Affin Islamic Bank Berhad'),
('Aham Asset Management Berhad (Formerly Known As Affin Hwang Asset Management Berhad)','Aham Asset Management Berhad (Formerly Known As Affin Hwang Asset Management Berhad)'),
('Aiiman Asset Management Sdn Bhd','Aiiman Asset Management Sdn Bhd'),
('Al Rajhi Banking & Investment Corporation (Malaysia) Berhad','Al Rajhi Banking & Investment Corporation (Malaysia) Berhad'),
('Alliance Bank (Malaysia) Berhad','Alliance Bank (Malaysia) Berhad'),
('Alliance Islamic Bank Berhad','Alliance Islamic Bank Berhad'),
('Amanah Saham Nasional Berhad','Amanah Saham Nasional Berhad'),
('Amanah Saham Sarawak Berhad','Amanah Saham Sarawak Berhad'),
('Amanahraya Investment Management Sdn Bhd','Amanahraya Investment Management Sdn Bhd'),
('Ambank Berhad','Ambank Berhad'),
('Ambank Islamic Berhad','Ambank Islamic Berhad'),
('Amfunds Management Berhad','Amfunds Management Berhad'),
('Aminvestment Bank Berhad','Aminvestment Bank Berhad'),
('Areca Capital Sdn Bhd','Areca Capital Sdn Bhd'),
('Astute Fund Management Berhad','Astute Fund Management Berhad'),
('Bank Islam Malaysia Berhad','Bank Islam Malaysia Berhad'),
('Bank Kerjasama Rakyat Malaysia Berhad','Bank Kerjasama Rakyat Malaysia Berhad'),
('Bank Muamalat Malaysia Berhad','Bank Muamalat Malaysia Berhad'),
('Bank Of China Malaysia Berhad','Bank Of China Malaysia Berhad'),
('Bank Simpanan Nasional','Bank Simpanan Nasional'),
('Bimb Investment Management Berhad','Bimb Investment Management Berhad'),
('Bos Wealth Management Malaysia Berhad','Bos Wealth Management Malaysia Berhad'),
('Cimb Bank Berhad','Cimb Bank Berhad'),
('Cimb Investment Bank Berhad','Cimb Investment Bank Berhad'),
('Cimb Islamic Bank Berhad','Cimb Islamic Bank Berhad'),
('Eastspring Investments Berhad','Eastspring Investments Berhad'),
('Franklin Templeton Gsc Asset Management Sdn. Bhd.','Franklin Templeton Gsc Asset Management Sdn. Bhd.'),
('Hong Leong Asset Management Bhd','Hong Leong Asset Management Bhd'),
('Hong Leong Bank Berhad','Hong Leong Bank Berhad'),
('Hong Leong Islamic Bank Berhad','Hong Leong Islamic Bank Berhad'),
('Hsbc Amanah Malaysia Berhad','Hsbc Amanah Malaysia Berhad'),
('Hsbc Bank (Malaysia) Berhad','Hsbc Bank (Malaysia) Berhad'),
('Ifast Capital Sdn Bhd','Ifast Capital Sdn Bhd'),
('Industrial And Commercial Bank Of China (Malaysia) Berhad','Industrial And Commercial Bank Of China (Malaysia) Berhad'),
('Inter-Pacific Asset Management Sdn Bhd','Inter-Pacific Asset Management Sdn Bhd'),
('Kaf Investment Funds Berhad','Kaf Investment Funds Berhad'),
('Kedah Islamic Asset Management Berhad','Kedah Islamic Asset Management Berhad'),
('Kenanga Investment Bank Berhad','Kenanga Investment Bank Berhad'),
('Kenanga Investors Berhad','Kenanga Investors Berhad'),
('Kuwait Finance House (M) Berhad','Kuwait Finance House (M) Berhad'),
('Malayan Banking Berhad','Malayan Banking Berhad'),
('Manulife Investment Management (M) Berhad','Manulife Investment Management (M) Berhad'),
('Maybank Asset Management Sdn Bhd','Maybank Asset Management Sdn Bhd'),
('Maybank Islamic Berhad','Maybank Islamic Berhad'),
('Mbsb Bank Berhad','Mbsb Bank Berhad'),
('Midf Amanah Asset Management Berhad','Midf Amanah Asset Management Berhad'),
('Muamalat Invest Sdn Bhd','Muamalat Invest Sdn Bhd'),
('Nomura Asset Management Malaysia Sdn. Bhd.','Nomura Asset Management Malaysia Sdn. Bhd.'),
('Nomura Islamic Asset Management Sdn. Bhd.','Nomura Islamic Asset Management Sdn. Bhd.'),
('Ocbc Al-Amin Berhad','Ocbc Al-Amin Berhad'),
('Ocbc Bank (Malaysia) Berhad','Ocbc Bank (Malaysia) Berhad'),
('Opus Asset Management Sdn Bhd','Opus Asset Management Sdn Bhd'),
('Pengurusan Kumipa Berhad','Pengurusan Kumipa Berhad'),
('Permodalan Bsn Berhad','Permodalan Bsn Berhad'),
('Pheim Unit Trusts Berhad','Pheim Unit Trusts Berhad'),
('Phillip Mutual Berhad','Phillip Mutual Berhad'),
('Pmb Investment Berhad','Pmb Investment Berhad'),
('Principal Asset Management Berhad','Principal Asset Management Berhad'),
('Ptb Unit Trust Berhad','Ptb Unit Trust Berhad'),
('Public Bank Berhad','Public Bank Berhad'),
('Public Mutual Berhad','Public Mutual Berhad'),
('Rhb Asset Management Sdn Bhd','Rhb Asset Management Sdn Bhd'),
('Rhb Bank Berhad','Rhb Bank Berhad'),
('Rhb Investment Bank Berhad','Rhb Investment Bank Berhad'),
('Rhb Islamic Bank Berhad','Rhb Islamic Bank Berhad'),
('Rhb Islamic International Asset Management Berhad','Rhb Islamic International Asset Management Berhad'),
('Saham Sabah Berhad','Saham Sabah Berhad'),
('Saturna Sdn Bhd','Saturna Sdn Bhd'),
('Standard Chartered Bank (Malaysia) Berhad','Standard Chartered Bank (Malaysia) Berhad'),
('Standard Chartered Saadiq Berhad','Standard Chartered Saadiq Berhad'),
('Ta Investment Management Berhad','Ta Investment Management Berhad'),
('Taurus Investment Management Berhad','Taurus Investment Management Berhad'),
('United Overseas Bank (Malaysia) Berhad','United Overseas Bank (Malaysia) Berhad'),
('Uob Asset Management (Malaysia) Berhad','Uob Asset Management (Malaysia) Berhad'),
('Uob Kay Hian Securities (M) Sdn Bhd','Uob Kay Hian Securities (M) Sdn Bhd'),
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
        ('Female', 'Female'),
        ('Male', 'Male'),        
        ('Prefer not to respond', 'Prefer not to respond'),
    ]

class BankForm(forms.ModelForm):
    def clean_account_no(self):
        account_no = str(self.cleaned_data.get('account_no', False))
        if re.search('[a-zA-Z]', account_no):
            raise ValidationError(
                _('Account no should not contain any characters'),
                params={'account_no': account_no},
            )

        return account_no

class SecuritiesInvestmentForm(forms.ModelForm):
    class Meta:
        model = SecuritiesInvestment
        fields = ('account_type',
                  'account_no',
                  'broker_name',
                  'account_value',
                )

class UnitTrustInvestmentForm(forms.ModelForm):
    class Meta:
        model = UnitTrustInvestment
        fields = ('unittrust_name',
                  'account_no',
                  'agent_name',
                  'agent_contact_no',
                  'account_value',
                )



BankModelFormset = modelformset_factory(
    Bank,
    form=BankForm,
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

class InsuranceForm(forms.ModelForm):
    def clean_nominee_name(self):
        nominee_name = str(self.cleaned_data.get('nominee_name', False))
        if re.search('[0-9]', nominee_name):
            raise ValidationError(
                _('Nominee name should not contain any numbers'),
                params={'nominee_name': nominee_name},
            )
        return nominee_name

InsuranceModelFormset = modelformset_factory(
    Insurance,
    form=InsuranceForm,
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


SecuritiesInvestmentModelFormset = modelformset_factory(
    SecuritiesInvestment,
    fields=('broker_name',
            'account_type',
            'account_no',
            'account_value',
            'user',
            ),
    extra=1,
    widgets={
        'account_type': forms.RadioSelect(choices=OVERSEAS_OR_LOCAL,attrs={
        }),
        'broker_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter broker name here'
        }),
        'account_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account no. here'
        }),
        'account_value': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account value here'
        }),
    }
)

UnitTrustInvestmentModelFormset = modelformset_factory(
    UnitTrustInvestment,
    fields=('unittrust_name',
            'account_no',
            'account_value',
            'agent_name',
            'agent_contact_no',
            'user',
            ),
    extra=1,
    widgets={
        'unittrust_name': forms.Select(choices=UNIT_TRUST_CHOICES,attrs={
            'class': 'form-control',
            'placeholder': 'Enter unit trust name here'
        }),
        'account_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account no. here'
        }),
        'agent_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter agent no. here'
        }),
        'agent_contact_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter contact no. here'
        }),
        'account_value': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account value here'
        }),
    }
)

from django.forms import BaseModelFormSet

PROPERTY_TYPE_CHOICES = [
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
        ('Land', 'Land'),
    ]

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_type',
            'residential_type',
            'address',
            'state',
            'postcode',
            'titleno',
            'spa_price',
            ]

    def clean_postcode(self):
        postcode = str(self.cleaned_data.get('postcode', False))
        if re.search('[a-zA-Z]', postcode):
            raise ValidationError(
                _('Postcode should not contain any characters'),
                params={'postcode': postcode},
            )
        if len(postcode) != 5:
            raise ValidationError(
                _('Only 5 digits allowed'),
                params={'postcode': postcode},
            )
        return postcode

PropertyModelFormset = modelformset_factory(
    Property,form=PropertyForm,
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
        'residential_type': forms.Select(choices=ResidentialType.objects.none(),attrs={
            # 'class': 'form-control',
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
            'default': 'Car',
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

CryptoModelFormset = modelformset_factory(
    Crypto,
    fields=('crypto_type',
            'wallet_name',
            'value',
            'user',
            ),
    extra=1,
    widgets={
        'crypto_type': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter crypto type here'
        }),
        'wallet_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter wallet name here'
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

    def clean_account_no(self):
        account_no = str(self.cleaned_data.get('account_no', False))
        if len(account_no) !=8:
            raise ValidationError(
                _('Account no should be 8 characters long'),
                params={'account_no': account_no},
            )

        return account_no

class EpfEditForm(forms.ModelForm):
    class Meta:
        model = Epf
        fields = ['account_no','account_value','nominee_name',]
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

    def clean_account_no(self):
        account_no = str(self.cleaned_data.get('account_no', False))
        if len(account_no) !=8:
            raise ValidationError(
                _('Account no should be 8 characters long'),
                params={'account_no': account_no},
            )

        return account_no

class SocsoForm(forms.ModelForm):
    class Meta:
        model = Socso
        fields = ['account_no','nominee_name','user']
        widgets={
            'account_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '900101100101'
        }),
            'nominee_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter nominee name here'
        }),
        }

    def clean_account_no(self):
        account_no = str(self.cleaned_data.get('account_no', False))
        if len(account_no) !=12:
            raise ValidationError(
                _('Account no should be 12 characters long'),
                params={'account_no': account_no},
            )

        return account_no


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
        'bank_name': forms.Select(choices=BANK_NAME_CHOICES,attrs={
            'class': 'form-control',
            'placeholder': 'Select a bank',
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
        'bank_name': forms.Select(choices=BANK_NAME_CHOICES,attrs={
            'class': 'form-control',
            'placeholder': 'Select a bank',
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
        'bank_name': forms.Select(choices=BANK_NAME_CHOICES,attrs={
            'class': 'form-control',
            'placeholder': 'Select a bank',
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
        'bank_name': forms.Select(choices=BANK_NAME_CHOICES,attrs={
            'class': 'form-control',
            'placeholder': 'Select a bank',
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

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_type','make_model','registration_no',]

class CryptoForm(forms.ModelForm):
    class Meta:
        model = Crypto
        fields = ['crypto_type','wallet_name','value',]

class OtherAssetForm(forms.ModelForm):
    class Meta:
        model = OtherAsset
        fields = ['name','value',]

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['bank_name','account_no','amount_outstanding',]


class PersonalLoanForm(forms.ModelForm):
    class Meta:
        model = PersonalLoan
        fields = ['bank_name','account_no','amount_outstanding','loan_tenure',]


class VehicleLoanForm(forms.ModelForm):
    class Meta:
        model = VehicleLoan
        fields = ['bank_name','account_no','amount_outstanding','loan_tenure',]


class PropertyLoanForm(forms.ModelForm):
    class Meta:
        model = PropertyLoan
        fields = ['bank_name','account_no','amount_outstanding','loan_tenure',]

class OtherLiabilityForm(forms.ModelForm):
    class Meta:
        model = OtherLiability
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

class NotifierForm(forms.ModelForm):
    class Meta:
        model = Notifier
        fields = [
            "name",
            "email",
            "ic",
            "contact_no",
            "relationship",
            "event",
        ]

class AccessListForm(forms.ModelForm):
    class Meta:
        model = Notifier
        fields = [
            "name",
            "email",
            "ic",
            "contact_no",
            "relationship",
            "event",
        ]

NotifierModelFormset = modelformset_factory(
    Notifier,
    fields=(
            "name",
            "email",
            "ic",
            "contact_no",
            "relationship",
            "event",
            "user",
            ),
    extra=1,
    widgets={
        'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter name here'
        }),
        'email': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email here'
        }),
        'ic': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter IC here'
        }),
        'contact_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter contact number here'
        }),
        'relationship': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter relationship here'
        }),
        'event': forms.CheckboxSelectMultiple(choices=EVENT_CHOICES,attrs={
            'placeholder': 'Enter event here'
        }),
    }
)

AccesslistModelFormset = modelformset_factory(
    AccessList,
    fields=(
            "name",
            "email",
            "ic",
            "contact_no",
            "relationship",
            "event",
            "user",
            ),
    extra=1,
    widgets={
        'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter name here'
        }),
        'email': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email here'
        }),
        'ic': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter IC here'
        }),
        'contact_no': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter contact number here'
        }),
        'relationship': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter relationship here'
        }),
        'event': forms.CheckboxSelectMultiple(choices=EVENT_CHOICES,attrs={
            'placeholder': 'Enter event here'
        }),
    }
)
# class NotifierForm(forms.Form):
#     notifier_name = forms.CharField()
#     notifier_email = forms.CharField()
#     notifier_ic = forms.CharField(required = False)
#     notifier_contactno = forms.CharField(required = False)
#     notifier_relationship = forms.CharField(required = False)
#     notifier_event = forms.MultipleChoiceField(choices=EVENT_CHOICES,required = False)
#     notifier_name_2 = forms.CharField(required = False)
#     notifier_email_2 = forms.CharField(required = False)
#     notifier_ic_2 = forms.CharField(required = False)
#     notifier_contactno_2 = forms.CharField(required = False)
#     notifier_relationship_2 = forms.CharField(required = False)
#     notifier_event_2 = forms.MultipleChoiceField(choices=EVENT_CHOICES,required = False)
#     yesno = forms.CharField(required = False)

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
