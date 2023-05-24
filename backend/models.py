from django.db import models
import uuid
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError 
from django.utils import timezone
from django_cryptography.fields import encrypt

# from ckeditor.fields import RichTextField
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class TimeStampedModel(models.Model): 
    """
    An abstract base class model that provides self-updating created and modified fields. 
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True) 

    class Meta:
        abstract = True

GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to respond', 'Prefer not to respond'),
    ]
class User(AbstractUser):
    """User model."""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=512,null=True, blank=True)
    postcode = models.CharField(max_length=512,null=True, blank=True)
    city = models.CharField(max_length=512,null=True, blank=True)
    state = models.CharField(max_length=512,null=True, blank=True)
    country = models.CharField(max_length=512,null=True, blank=True)
    gender = models.CharField(max_length=100, blank=True)
    age = models.CharField(max_length=100, blank=True)
    marital = models.CharField(max_length=100, blank=True)
    referral_code = models.CharField(max_length=100, blank=True)
    # user_permission +
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

"""Custom User Model End"""

class Item(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_items')
    data = models.JSONField()
    item_type = models.CharField(max_length=128)
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)

class Subscription(TimeStampedModel):
    plan = models.CharField(max_length=128)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_subscriptions')




""" V2 Assets & Liabilities """
class Epf(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_epf')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    account_no = models.CharField(max_length=128)
    account_value = models.FloatField(max_length=128,null=True,blank=True)
    nominee_name = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.account_no

    class Meta:
        verbose_name_plural = "EPF"

class Socso(TimeStampedModel): 
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_socso')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    account_no = models.CharField(max_length=128)
    nominee_name = models.CharField(max_length=128,null=True,blank=True)
    account_value = models.FloatField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.account_no

    class Meta:
        verbose_name_plural = "Socso"

class Bank(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_bankaccount')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    account_type = models.CharField(max_length=128)
    bank_name = models.CharField(max_length=128)
    account_no = models.CharField(max_length=128)
    account_value = models.FloatField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.bank_name

class Insurance(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_insurance')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    insurance_type = models.CharField(max_length=128)
    provider = models.CharField(max_length=128)
    policy_no = models.CharField(max_length=128)
    nominee_name = models.CharField(max_length=128,null=True,blank=True)
    sum_insured = models.FloatField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.provider

class Investment(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_investment')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    account_type = models.CharField(max_length=128)
    bank_name = models.CharField(max_length=128)
    account_no = models.CharField(max_length=128)
    account_value = models.FloatField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.bank_name

class SecuritiesInvestment(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_securities_investment')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    account_type = models.CharField(max_length=128)
    broker_name = models.CharField(max_length=128)
    account_no = models.CharField(max_length=128)
    account_value = models.FloatField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.account_type

class UnitTrustInvestment(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_unittrust_investment',null=True)
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    unittrust_name = models.CharField(max_length=128)
    account_no = models.CharField(max_length=128)
    agent_name = models.CharField(max_length=128,null=True,blank=True)
    agent_contact_no = models.CharField(max_length=128,null=True,blank=True)
    account_value = models.FloatField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.unittrust_name

class Property(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_property')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    property_type = models.CharField(max_length=128,null=True,blank=True)
    residential_type = models.CharField(max_length=128,null=True,blank=True)
    address = models.CharField(max_length=128,null=True,blank=True)
    state = models.CharField(max_length=128,null=True,blank=True)
    postcode = models.CharField(max_length=128,null=True,blank=True)
    titleno = models.CharField(max_length=128,null=True,blank=True)
    spa_price = models.FloatField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.property_type

    class Meta:
        verbose_name_plural = "Properties"

class Vehicle(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_vehicle')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    vehicle_type = models.CharField(max_length=128,null=True,blank=True)
    make_model = models.CharField(max_length=128,null=True,blank=True)
    registration_no = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.vehicle_type

class OtherAsset(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_otherassets')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=128)
    value = models.FloatField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.name

class Crypto(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_crypto')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    crypto_type = models.CharField(max_length=128)
    wallet_name = models.CharField(max_length=128)
    value = models.FloatField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.crypto_type

class CreditCard(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_creditcard')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    bank_name = models.CharField(max_length=128)
    account_no = models.CharField(max_length=128,null=True,blank=True)
    amount_outstanding = models.FloatField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.bank_name

class PersonalLoan(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_personalloan')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    bank_name = models.CharField(max_length=128)
    account_no = models.CharField(max_length=128,null=True,blank=True)
    amount_outstanding = models.FloatField(max_length=128,null=True,blank=True)
    loan_tenure = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.bank_name

class VehicleLoan(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_vehicleloan')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    bank_name = models.CharField(max_length=128)
    account_no = models.CharField(max_length=128,null=True,blank=True)
    amount_outstanding = models.FloatField(max_length=128,null=True,blank=True)
    loan_tenure = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.bank_name

class PropertyLoan(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_propertyloan')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    bank_name = models.CharField(max_length=128)
    account_no = models.CharField(max_length=128,null=True,blank=True)
    amount_outstanding = models.FloatField(max_length=128,null=True,blank=True)
    loan_tenure = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.bank_name

class OtherLiability(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_otherliabilities')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=128)
    value = models.FloatField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Other Liabilities"

class Notifier(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_notifier')
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=128,null=True,blank=True)
    ic = models.CharField(max_length=128,null=True,blank=True)
    contact_no = models.CharField(max_length=128,null=True,blank=True)
    relationship = models.CharField(max_length=128,null=True,blank=True)
    event = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.name

class AccessList(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_accesslist')
    name = models.CharField(max_length=128)
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=128,null=True,blank=True)
    ic = models.CharField(max_length=128,null=True,blank=True)
    contact_no = models.CharField(max_length=128,null=True,blank=True)
    relationship = models.CharField(max_length=128,null=True,blank=True)
    event = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.name

## Property 
class PropertyType(TimeStampedModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class ResidentialType(TimeStampedModel):
    property_type = models.ForeignKey('backend.PropertyType',on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

""" V2 Assets & Liabilities """





