from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProfileDetails

@receiver(signal=post_save, sender=User)
def create_profile_on_register(sender, instance, created, **kwa):
    if created:
        ProfileDetails.objects.create(user=instance)
        instance.profiledetails.save()
