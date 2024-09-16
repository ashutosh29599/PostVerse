from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    # TODO: Text or photo -- either can be optional, but not both.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to="post_photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.text[:10]}"  # type: ignore
