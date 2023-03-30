from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_measurement.models import MeasurementField
from measurement.measures import Weight


class User(AbstractUser):

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'{self.username}'

    class Meta:
        get_latest_by = ('username',)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    body_weight = MeasurementField(measurement=Weight, null=True, blank=True)  # TODO  Set a default


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
