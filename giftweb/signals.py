
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserActivity



@receiver(post_save, sender=UserActivity)  # Replace `YourModel` with the model you want to track
def log_user_activity(sender, instance, created, **kwargs):
    if created:
        action = f"Created {instance.__class__.__name__} with ID {instance.id}"
    else:
        action = f"Updated {instance.__class__.__name__} with ID {instance.id}"

    UserActivity.objects.create(user=instance.user, action=action)


