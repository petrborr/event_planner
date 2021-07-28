from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from event_planner.accounts.models import UserProfile

UserModel = get_user_model()

#
# @receiver(post_save, sender=UserModel)
# def user_created(sender, instance, created, **kwargs):
#     if created:
#         profile = UserProfile(
#             user=instance,
#         )
#
#         profile.save()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=UserModel)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()
