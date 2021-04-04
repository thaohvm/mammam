from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    ingredients = models.TextField(max_length=500, blank=True)
    steps = models.TextField(max_length=4000, blank=True)
    extra = models.TextField(max_length=4000, blank=True)
    image = models.ForeignKey(
        "Image", on_delete=models.SET_NULL, null=True, related_name="image"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user}"


class Image(models.Model):
    file = models.FileField(upload_to="images")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} at {self.file.url}"
