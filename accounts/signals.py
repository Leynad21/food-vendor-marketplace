from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance) # this created user profile
    else:
        # User is updated
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create the userProfile if not exist
            UserProfile.objects.create(user=instance) # Profile did not existed but was created


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
    # print(instance.username, "this user is being saved")



# post_save.connect(post_save_create_profile_receiver, sender=User)