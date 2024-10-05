from django.db.models import Max
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import User, Profile, AccountDetails

@receiver(pre_save, sender=AccountDetails)
def create_account_no(sender, instance, *args, **kwargs):
    # checks if the user has an account number and the user is not staff or superuser
    if not instance.account_no and not (instance.user.is_staff or instance.user.is_superuser):
        # gets the largest account number
        largest = AccountDetails.objects.all().aggregate(
            Max("account_no")
        )['account_no__max']

        if largest:
            # creates a new account number
            instance.account_no = largest + 1
        else:
            # if there is no other user, sets the user's account number to 10000000.
            instance.account_no = 10000000

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, *args, **kwargs):
    if created:
        # Check if a Profile already exists for the user
        if not Profile.objects.filter(user=instance).exists():
            # Create a welcome message and send it to the user's email
            subject = 'Welcome to Our store'
            message = render_to_string('welcome_email.html', {'user': instance})
            plain_message = strip_tags(message)
            from_email = 'MS_hEOIPz@zorevinacart.store'  # Set your email address
            to_email = instance.email

            send_mail(subject, plain_message, from_email, [to_email], html_message=message)

            # Create a profile for the user
            Profile.objects.create(user=instance)
