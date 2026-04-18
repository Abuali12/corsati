from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
from django.dispatch import receiver
from core.models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(user_signed_up)
def create_profile_social(request, user, **kwargs):
    Profile.objects.get_or_create(user=user)