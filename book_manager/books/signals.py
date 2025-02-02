from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        social_account = SocialAccount.objects.filter(user=instance, provider="google").first()
        profile_picture = social_account.extra_data.get("picture") if social_account else None
        Profile.objects.create(user=instance, profile_picture=profile_picture)
