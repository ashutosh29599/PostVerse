from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    bio = models.TextField(max_length=240, blank=True, null=True)
    photo = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username   # type: ignore
