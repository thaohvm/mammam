from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_age = models.TextField(max_length=1000, blank=True)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000, blank=True)
    ingredients = models.TextField(max_length=1000, blank=True)
    steps = models.TextField()
    image = models.ImageField(upload_to="uploads/images", blank=True)
