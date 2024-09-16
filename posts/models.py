from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Post(models.Model):
    # TODO: Text or photo -- either can be optional, but not both.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField(max_length=240, blank=True, null=True)
    photo = models.ImageField(upload_to="post_photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        message = f"{self.user.username}"  # type: ignore

        if self.text:
            message += f" - {self.text[:10]}"
        if self.photo:
            message += f" - {self.photo.name.split('/')[-1]}"

        return message

    def clean(self):
        if not self.text and not self.photo:
            return ValidationError('Either text or a photo must be provided for a post.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
