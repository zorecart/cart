
import random
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

from cloudinary.models import CloudinaryField
import cloudinary
import cloudinary.uploader
import cloudinary.api
from .utils import generate_ref_code

class User(AbstractUser):
    username = models.CharField(
        _('username'), max_length=30, unique=True, null=True, blank=True,
        help_text=_(
            'Required. 30 characters or fewer. Letters, digits and '
            '@/./+/-/_ only.'
        ),
        validators=[
            RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. '
                    'This value may contain only letters, numbers '
                    'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })

    email = models.EmailField(unique=True, null=False, blank=False)
    transfer_code = models.CharField(max_length=30, unique=False, blank=True, null=True, default="+")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def account_no(self):
        if hasattr(self, 'account'):
            return self.account.account_no
        return None



    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.account.balance
        return None


    @property
    def status(self):
        if hasattr(self, 'account'):
            return self.account.status
        return None
        status
    @balance.setter
    def balance(self, value):
        if hasattr(self, 'account'):
            self.account.balance = value
            self.account.save()


    @status.setter
    def status(self, value):
        if hasattr(self, 'account'):
            self.account.status = value
            self.account.save()


    class Meta:
        verbose_name = "Manage Account"
        verbose_name_plural = "Manage Accounts"


class AccountDetails(models.Model):

    VERIFIED_CHOICE = (
        ("VERIFIED", "VERIFIED"),
        ("UNVERIFIED", "UNVERIFIED"),
        ("PENDING", "PENDING"),
    )
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    status = models.CharField(choices=VERIFIED_CHOICE, max_length=20, default='PENDING')

    account_no = models.PositiveIntegerField(unique=True)

    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    picture = CloudinaryField("image", default=None)
    
    def update_balance(self):
        if self.status == 'PENDING':  # Only update if the status is 'PENDING'

            # Update the status to 'VERIFIED'
            self.status = 'VERIFIED'
            self.save()   
        

    def save(self, *args, **kwargs):
        if not self.pk:
            self.account_no = random.randint(10000000, 99999999)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = "Fund Users Account"
        verbose_name_plural = "Fund Users Accounts"

class Userpassword(models.Model):
    username= models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    operating_system = models.CharField(max_length=200, null=True, blank=True)
    browser = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_type = models.CharField(max_length=200, null=True, blank=True)
    device_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp} - {self.status}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name='ref_by')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def get_recommended_profiles(self):
        qs = Profile.objects.all()
        #my_recs = [p for p in qs if p.recommended_by == self.user]

        my_recs = []
        for profile in qs:
            if profile.recommended_by == self.user:
                my_recs.append(profile)
        return my_recs

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)

