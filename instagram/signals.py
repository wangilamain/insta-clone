from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = Profile.objects.create(users=kwargs['instance'])
post_save.connect(create_profile, sender=User)