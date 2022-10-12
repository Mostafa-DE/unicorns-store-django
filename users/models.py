from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.contrib.auth import get_user_model


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="profile")
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    building_number = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
