from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile

# Signal to create or save the UserProfile when a CustomUser is created/updated
@receiver(post_save, sender=CustomUser)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create UserProfile if the user is created
        UserProfile.objects.create(user=instance)
    else:
        # Save UserProfile when the user is updated
        instance.userprofile.save()
