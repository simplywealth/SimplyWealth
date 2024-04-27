from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Transaction
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
import uuid
from django.utils import timezone

@receiver(user_signed_up)
def create_user_profile_and_transaction(sender, request, user, **kwargs):
    print("Handling signup")
    profile, created = UserProfile.objects.get_or_create(user=user)
    print(f"Profile created: {profile}, created: {created}")
    created = True
    if created:
        # if not SocialAccount.objects.filter(user=user).exists():
            # Handle native app signup
        Transaction.objects.create(
            transaction_id=uuid.uuid4(),
            user=profile,
            amount=1000,
            timestamp=timezone.now()
        )

# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if not SocialAccount.objects.filter(user=instance).exists():
#             print("Handling native app authentication")
#             UserProfile.objects.get_or_create(user=instance)
