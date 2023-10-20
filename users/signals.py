from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile, ProfileStatus

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        ProfileStatus.objects.create(profile=profile)

