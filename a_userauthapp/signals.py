
from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import User, StudentProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)
