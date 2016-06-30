from django.db import models
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(user_signed_up)
def create_user_profile(sender, **kwargs):
    """Creates a user profile after user signup (using django-allauth)"""
    profile = UserProfile(user=kwargs['user'])
    profile.save()
