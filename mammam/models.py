import os
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


def get_random_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("images/", filename)


class User(AbstractUser):
    pass


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    age = models.TextField(max_length=100, blank=True)
    ingredients = models.TextField(max_length=500)
    steps = models.TextField(max_length=4000)
    image = models.ForeignKey(
        "Image", on_delete=models.SET_NULL, null=True, related_name="image"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user}"


class Image(models.Model):
    file = models.FileField(upload_to=get_random_file_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} at {self.file.url}"
