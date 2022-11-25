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
    marital = models.CharField(max_length=100, blank=True)
    # groups = 
    # user_permission +
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

"""Custom User Model End"""

class Item(TimeStampedModel):
    ITEM_TYPE_CHOICES = [
    ('Assets', 'Assets'),
    ('Liabilities', 'Liabilities'),
]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_items')
    data = models.JSONField()
    item_type = models.CharField(choices=ITEM_TYPE_CHOICES,max_length=128)
    created_by = models.ForeignKey('backend.User',on_delete=models.CASCADE,null=True)

class Subscription(TimeStampedModel):
    plan = models.CharField(max_length=128)
    user = models.ForeignKey('backend.User',on_delete=models.CASCADE,related_name='user_subscriptions')

