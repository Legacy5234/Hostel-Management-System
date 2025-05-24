
from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import User, StudentProfile
from b_hostels.models import Hostel, Room

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)


@receiver(post_save, sender=Hostel)
def create_rooms_for_hostel(sender, instance, created, **kwargs):
    if created:
        for i in range(1, 111):  # creates 20 rooms numbered 1-20
            Room.objects.create(
                hostel=instance,
                room_number=str(i).zfill(3),  # eg: '001', '002' etc.
                capacity=2
            )
